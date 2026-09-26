import asyncio
from collections.abc import Awaitable, Callable


class BoundedStream:
    """Async bounded stream with explicit backpressure and graceful shutdown."""

    def __init__(self, maxsize: int = 1024) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be positive")
        self._queue: asyncio.Queue[object] = asyncio.Queue(maxsize=maxsize)
        self._closed = False

    async def publish(self, item: object) -> None:
        if self._closed:
            raise RuntimeError("stream is closed")
        await self._queue.put(item)

    async def consume(self, handler: Callable[[object], Awaitable[None]]) -> None:
        while not self._closed or not self._queue.empty():
            try:
                item = await asyncio.wait_for(self._queue.get(), timeout=0.25)
            except TimeoutError:
                continue
            try:
                await handler(item)
            finally:
                self._queue.task_done()

    async def drain(self) -> None:
        await self._queue.join()

    def close(self) -> None:
        self._closed = True
