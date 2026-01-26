from dataclasses import dataclass
from typing import Callable

# TODO implement logging for this.


@dataclass
class Event:
    """Base event dataclass that stores nothing."""


class EventManager:
    """Centralized handler for `emitters` and `listeners`, pipes `Event`s."""

    listeners: dict[type[Event], list[Callable[[Event], None]]]

    def __init__(self) -> None:
        self.listeners = {}

    def listen(
        self, event_type: type[Event], callback: Callable[[Event], None]
    ) -> None:
        """Register an event listener with a callback"""

        if self.listeners.get(event_type) is None:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event: Event) -> None:
        """Emit an event."""

        event_type: type[Event] = type(event)
        if self.listeners.get(event_type) is None:
            return
        callbacks = self.listeners[event_type]

        for callback in callbacks:
            callback(event)
