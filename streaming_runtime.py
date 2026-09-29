import asyncio
from collections.abc import Awaitable, Callable


class BoundedStream:
    """Async bounded stream with explicit backpressure and graceful shutdown."""

    def __init__(self, maxsize: int = 1024) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be positive")
        self._queue: asyncio.Queue[object] = asyncio.Queue(maxsize=maxsize)
        self._closed = False
        self._failure: Exception | None = None

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
            except Exception as exc:
                self._failure = exc
                self._closed = True
                # A failed single consumer cannot leave queued items blocking drain forever.
                while not self._queue.empty():
                    self._queue.get_nowait()
                    self._queue.task_done()
                raise
            finally:
                self._queue.task_done()

    async def drain(self) -> None:
        await self._queue.join()
        if self._failure is not None:
            raise RuntimeError("stream consumer failed") from self._failure

    def close(self) -> None:
        self._closed = True
