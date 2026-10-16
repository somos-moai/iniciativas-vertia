"""Protect response bytes and framing when bounding large socket writes."""
import asyncio
import gzip
import json
import pytest
from backend.transport import ResponseChunkMiddleware

@pytest.mark.parametrize("compressed",[False,True])
def test_large_json_response_survives_bounded_writes(compressed):
    source=json.dumps({"rows":[{"id":i,"name":f"Empresa {i}","detail":"Cobertura urbana y trazabilidad"} for i in range(20000)]}).encode()
    wire=gzip.compress(source) if compressed else source
    emitted=[]

    async def endpoint(scope,receive,send):
        headers=[(b"content-length",str(len(wire)).encode()),(b"content-type",b"application/json")]
        if compressed: headers.append((b"content-encoding",b"gzip"))
        await send({"type":"http.response.start","status":200,"headers":headers})
        await send({"type":"http.response.body","body":wire,"more_body":False})

    async def send(message): emitted.append(message)
    async def receive(): return {"type":"http.request","body":b"","more_body":False}
    asyncio.run(ResponseChunkMiddleware(endpoint)({"type":"http"},receive,send))
    received=b"".join(event.get("body",b"") for event in emitted if event["type"]=="http.response.body")
    assert received==wire
    assert len(received)==int(dict(emitted[0]["headers"])[b"content-length"])
    assert not emitted[-1]["more_body"]
    assert json.loads(gzip.decompress(received) if compressed else received)["rows"][-1]["id"]==19999

def test_existing_stream_preserves_its_final_event():
    emitted=[]
    async def endpoint(scope,receive,send):
        await send({"type":"http.response.start","status":200,"headers":[]})
        await send({"type":"http.response.body","body":b"A"*150000,"more_body":True})
        await send({"type":"http.response.body","body":b"end","more_body":False})
    async def send(message): emitted.append(message)
    async def receive(): return {"type":"http.request","body":b"","more_body":False}
    asyncio.run(ResponseChunkMiddleware(endpoint)({"type":"http"},receive,send))
    assert b"".join(m.get("body",b"") for m in emitted)==b"A"*150000+b"end"
    assert emitted[-1]["more_body"] is False
    assert all(m["more_body"] for m in emitted[1:-1])
