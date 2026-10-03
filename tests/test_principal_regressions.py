import asyncio

import pytest

from streaming_runtime import BoundedStream


def test_drain_timeout_reports_missing_consumer():
    async def scenario():
        stream = BoundedStream(maxsize=1)
        await stream.publish("message")
        with pytest.raises(TimeoutError):
            await stream.drain(timeout=0.01)

    asyncio.run(scenario())


def test_drain_rejects_invalid_timeout():
    async def scenario():
        stream = BoundedStream()
        with pytest.raises(ValueError):
            await stream.drain(timeout=0)

    asyncio.run(scenario())
