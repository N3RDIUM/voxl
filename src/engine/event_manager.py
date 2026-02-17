import asyncio
import os
from dataclasses import dataclass
from typing import Callable, TypeVar, cast

# TODO implement logging for this?


@dataclass
class Event:
    """Base event dataclass that stores nothing."""


E = TypeVar("E", bound=Event)


class EventManager:
    """Centralized handler for `emitters` and `listeners`, pipes `Event`s."""

    listeners: dict[type[Event], list[Callable[[Event], None]]]
    threadsafe_listeners: dict[type[Event], list[Callable[[Event], None]]]
    _semaphore: asyncio.Semaphore

    def __init__(self) -> None:
        self.listeners = {}
        self.threadsafe_listeners = {}
        self._semaphore = asyncio.Semaphore(os.cpu_count() or 1)

    def listen(
        self,
        event_type: type[E],
        callback: Callable[[E], None],
        threadsafe: bool = False,
    ) -> None:
        if not threadsafe:
            self._listen(event_type, callback)
            return
        self._listen_threadsafe(event_type, callback)

    def _listen(
        self, event_type: type[E], callback: Callable[[E], None]
    ) -> None:
        """Register an event listener with a callback"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(
            cast(Callable[[Event], None], callback)
        )

    def _listen_threadsafe(  # TODO typehint with Coroutine instead of Callable
        self, event_type: type[E], callback: Callable[[E], None]
    ) -> None:
        """Register an event listener with a callback"""
        if event_type not in self.threadsafe_listeners:
            self.threadsafe_listeners[event_type] = []
        self.threadsafe_listeners[event_type].append(
            cast(Callable[[Event], None], callback)
        )

    # TODO error handling

    def _emit(self, event: Event) -> None:
        event_type: type[Event] = type(event)
        if event_type not in self.listeners:
            return
        callbacks = self.listeners[event_type]
        for callback in callbacks:
            callback(event)

    async def _emit_parallel(self, event: Event) -> None:
        event_type: type[Event] = type(event)

        if event_type not in self.threadsafe_listeners:
            return

        callbacks = self.listeners[event_type]

        async def run_callback(callback: Callable[[Event], None]) -> None:
            async with self._semaphore:
                await asyncio.to_thread(callback, event)

        tasks = [run_callback(callback) for callback in callbacks]

        _ = await asyncio.gather(*tasks)

    def emit(self, event: Event) -> None:
        _ = asyncio.create_task(self._emit_parallel(event))
        self._emit(event)
