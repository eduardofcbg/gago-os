import asyncio
from contextlib import suppress
from functools import wraps, partial


def run_in_executor(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, partial(f, *args, **kwargs))

    return wrapped


async def cancel_gen(agen):
    task = asyncio.create_task(agen.__anext__())
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    await agen.aclose()
