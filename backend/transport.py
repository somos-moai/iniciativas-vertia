"""Bound large ASGI writes without changing HTTP framing or response content."""
import asyncio

class ResponseChunkMiddleware:
    """Keep socket backpressure active for regional JSON and document downloads.

    Content-Length remains the original length (including gzip when enabled).
    Splitting ASGI body events does not add HTTP chunked framing to a response
    that already declares a Content-Length.
    """

    def __init__(self, app, chunk_size=64*1024):
        self.app=app
        self.chunk_size=chunk_size

    async def __call__(self,scope,receive,send):
        if scope["type"]!="http":
            await self.app(scope,receive,send)
            return

        async def bounded_send(message):
            if message["type"]!="http.response.body" or len(message.get("body",b""))<=self.chunk_size:
                await send(message)
                return
            body=message["body"]
            for offset in range(0,len(body),self.chunk_size):
                final=offset+self.chunk_size>=len(body)
                await send({**message,"body":body[offset:offset+self.chunk_size],"more_body":bool(message.get("more_body",False)) or not final})
                await asyncio.sleep(0)

        await self.app(scope,receive,bounded_send)
