import asyncio


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        try:
            while True:  # Loop indefinitely to call the callback periodically
                await asyncio.sleep(self._timeout)
                await self._callback()
        except asyncio.CancelledError:
            # Gracefully handle cancellation
            pass

    def cancel(self):
        self._task.cancel()
