from dataclasses import dataclass
from typing import Callable, TypeVar, cast

# TODO implement logging for this.


@dataclass
class Event:
    """Base event dataclass that stores nothing."""


E = TypeVar("E", bound=Event)


class EventManager:
    """Centralized handler for `emitters` and `listeners`, pipes `Event`s."""

    listeners: dict[type[Event], list[Callable[[Event], None]]]

    def __init__(self) -> None:
        self.listeners = {}

    def listen(
        self, event_type: type[E], callback: Callable[[E], None]
    ) -> None:
        """Register an event listener with a callback"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(
            cast(Callable[[Event], None], callback)
        )

    def emit(self, event: Event) -> None:
        """Emit an event."""
        event_type: type[Event] = type(event)
        if event_type not in self.listeners:
            return
        callbacks = self.listeners[event_type]
        for callback in callbacks:
            callback(event)
