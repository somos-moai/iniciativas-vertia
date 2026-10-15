"""PostgreSQL only. Credentials are supplied by the process, never read from files."""
import os
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, create_engine, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase):
    pass

class Record(Base):
    __tablename__ = "vertia_demo_records"
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    app: Mapped[str] = mapped_column(String(24), index=True)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    data: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Meta(Base):
    __tablename__ = "vertia_demo_meta"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[dict] = mapped_column(JSONB)

def database_url():
    url = os.environ.get("DATABASE_URL", "")
    if not url.startswith(("postgresql://", "postgresql+psycopg://")):
        raise RuntimeError("DATABASE_URL debe apuntar a PostgreSQL dedicado de demostración; SQLite no está permitido.")
    return url.replace("postgresql://", "postgresql+psycopg://", 1)

def make_engine():
    return create_engine(database_url(), pool_pre_ping=True, pool_size=5, max_overflow=5)

def initialize(engine):
    from .seed import seed
    # Serialize DDL and seed together, including simultaneous ASGI worker startup.
    with engine.begin() as connection:
        connection.execute(text("SELECT pg_advisory_xact_lock(84261015)"))
        Base.metadata.create_all(connection)
        with sessionmaker(bind=connection)() as session, session.begin():
            if not session.get(Meta, "seed_v1"):
                seed(session)
                session.add(Meta(key="seed_v1", value={"version": 1, "synthetic": True}))
