import asyncio
import tkinter as tk

class TkinterLoop(asyncio.AbstractEventLoop):
    def __init__(self, root):
        self.root = root
        self._running = False
        self._stopped = asyncio.Event()
        self._queue = asyncio.Queue()

    def run_forever(self):
        self._running = True
        while self._running:
            self.root.update()
            self._process_queue()

    def run_until_complete(self, future):
        asyncio.ensure_future(future, loop=self)
        self.run_forever()

    def stop(self):
        self._running = False
        self._stopped.set()

    def is_running(self):
        return self._running

    def is_closed(self):
        return not self._running

    def close(self):
        self.stop()

    def _process_queue(self):
        while not self._queue.empty():
            handle = self._queue.get_nowait()
            handle._run()

    def call_soon(self, callback, *args, context=None):
        handle = asyncio.Handle(callback, args, self)
        self._queue.put_nowait(handle)
        return handle

    def call_later(self, delay, callback, *args, context=None):
        self.root.after(int(delay * 1000), lambda: self.call_soon(callback, *args))

    def call_at(self, when, callback, *args, context=None):
        now = self.time()
        delay = max(0, when - now)
        return self.call_later(delay, callback, *args)

    def time(self):
        return asyncio.get_event_loop().time()

    def create_task(self, coro):
        return asyncio.Task(coro, loop=self)

    def create_future(self):
        return asyncio.Future(loop=self)
