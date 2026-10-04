import asyncio

import pytest

from streaming_runtime import BoundedStream


def test_failed_consumer_does_not_leave_drain_hanging():
    async def scenario():
        stream = BoundedStream(maxsize=3)
        await stream.publish("first")
        await stream.publish("second")
        stream.close()

        async def fail(_):
            raise ValueError("broken handler")

        with pytest.raises(ValueError, match="broken handler"):
            await stream.consume(fail)
        with pytest.raises(RuntimeError, match="consumer failed"):
            await asyncio.wait_for(stream.drain(), timeout=0.5)
        with pytest.raises(RuntimeError, match="closed"):
            await stream.publish("third")

    asyncio.run(scenario())
