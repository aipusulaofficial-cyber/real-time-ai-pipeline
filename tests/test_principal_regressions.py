import pytest

from streaming_runtime import BoundedStream


@pytest.mark.asyncio
async def test_drain_timeout_reports_missing_consumer():
    stream = BoundedStream(maxsize=1)
    await stream.publish("message")
    with pytest.raises(TimeoutError):
        await stream.drain(timeout=0.01)


@pytest.mark.asyncio
async def test_drain_rejects_invalid_timeout():
    stream = BoundedStream()
    with pytest.raises(ValueError):
        await stream.drain(timeout=0)
