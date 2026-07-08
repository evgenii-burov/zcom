from enum import Enum, auto
from typing import Callable


class Event(Enum):
    STATE_TRANSITION = auto()
    ENTITY_PLACED = auto()
    UNIT_MOVED = auto()
    PROJECTILE_SHOT = auto()
    UNIT_DIED = auto()


class EventBus:
    def __init__(self):
        self._observers: dict[Event, list[Callable]] = {event: [] for event in Event}

    def subscribe(self, event: Event, fn: Callable) -> None:
        self._observers[event].append(fn)

    def unsubscribe(self, event: Event, fn: Callable) -> None:
        self._observers[event].remove(fn)

    def emit(self, event: Event, **data) -> None:
        for fn in self._observers[event]:
            fn(**data)