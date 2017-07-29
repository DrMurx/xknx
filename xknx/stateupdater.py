import asyncio

class StateUpdater():

    def __init__(self,
                 xknx,
                 timeout=3600,
                 start_timeout=10):
        """Initialize StateUpdater class."""
        self.xknx = xknx
        self.timeout = timeout
        self.start_timeout = start_timeout

    @asyncio.coroutine
    def start(self):
        """Start StateUpdater."""
        self.xknx.loop.create_task(
            self.run())

    @asyncio.coroutine
    def run(self):
        """StateUpdater thread. Endless loop for updating states."""
        yield from asyncio.sleep(self.start_timeout)
        print("Starting Update Thread")
        while True:
            yield from self.xknx.devices.sync()
            yield from asyncio.sleep(self.timeout)
