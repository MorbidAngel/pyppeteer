import asyncio
from typing import Iterable, Union, AsyncIterable

from websockets import connect, WebSocketClientProtocol, Data


class WebsocketTransport:
    def __init__(self, ws: WebSocketClientProtocol):
        self.onmessage = None
        self.onclose = None
        self.ws = ws

    @classmethod
    async def create(cls, uri: str, loop: asyncio.AbstractEventLoop = None) -> 'WebsocketTransport':
        return cls(await connect(
            uri=uri,
            ping_interval=None,
            max_size=256 * 1024 * 1024,  # 256Mb
            loop=loop
        ))

    async def send(self, message: Union[Data, Iterable[Data], AsyncIterable[Data]]) -> None:
        await self.ws.send(message)

    async def close(self, code: int = 1000, reason: str = '') -> None:
        await self.ws.close(code=code, reason=reason)
        if self.onclose:
            await self.onclose()

    async def recv(self) -> Data:
        data = await self.ws.recv()
        if self.onmessage and data:
            await self.onmessage(data)
        return Data
