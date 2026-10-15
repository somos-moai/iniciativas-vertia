"""Prepare NEW Vertia demo resources on the authorized MoAI VPS.

Run remotely as root. Existing PostgreSQL roles/databases and websites are never
modified. Credentials are generated remotely and stored only in a private .env.
"""
from pathlib import Path
import json
import os
import pwd
import secrets
import subprocess

ROOT = Path('/home/moai/iniciativas-vertia')
ROLE = 'vertia_demo'
DB = 'vertia_demo'

def run(args, **kw):
    return subprocess.run(args, check=True, text=True, capture_output=True, **kw)

def pg(sql):
    return run(['sudo', '-u', 'postgres', 'psql', '-X', '-v', 'ON_ERROR_STOP=1', '-At'], input=sql).stdout.strip()

ROOT.mkdir(mode=0o750, parents=False, exist_ok=True)
env = ROOT / '.env'
account = pwd.getpwnam('moai')
if env.exists():
    print('Private environment already exists; preserved.')
else:
    if pg(f"SELECT 1 FROM pg_roles WHERE rolname='{ROLE}'") or pg(f"SELECT 1 FROM pg_database WHERE datname='{DB}'"):
        raise SystemExit('Resource name already in use without matching environment; manual review required.')
    password = secrets.token_urlsafe(36)
    # Password never appears in process arguments or logs.
    pg(f"CREATE ROLE {ROLE} LOGIN PASSWORD '{password}' NOSUPERUSER NOCREATEDB NOCREATEROLE;\nCREATE DATABASE {DB} OWNER {ROLE};")
    with env.open('x', encoding='utf-8') as handle:
        os.chmod(env, 0o600)
        handle.write(f'DATABASE_URL=postgresql+psycopg://{ROLE}:{password}@127.0.0.1:5432/{DB}\n')
        handle.write('PROPOSALS_DIR=/home/moai/iniciativas-vertia/deliverables\n')
    os.chown(env, account.pw_uid, account.pw_gid)
    print('Exclusive PostgreSQL role/database created; private environment stored.')
os.chown(ROOT, account.pw_uid, account.pw_gid)
if not (ROOT / '.venv' / 'bin' / 'python').exists():
    run(['sudo', '-u', 'moai', 'python3', '-m', 'venv', str(ROOT / '.venv')])
print(json.dumps({'project': str(ROOT), 'database': DB, 'role': ROLE, 'venv': str(ROOT / '.venv')}, ensure_ascii=False))
