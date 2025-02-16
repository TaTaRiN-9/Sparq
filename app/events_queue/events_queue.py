import asyncio

from fastapi import WebSocket


async def queue_getter(queue_number: int, queue):
    return queue_number, await queue.get()


class EventsQueue:
    def __init__(self):
        self._events_queue = asyncio.Queue()
        self._connections = asyncio.Queue()
        self._handlers = {}
        self.connections: list[tuple[WebSocket, str]] = []

    async def run_proccesing(self):
        while True:
            event = await self._events_queue.get()
            await event.process(self)
            self._events_queue.task_done()
