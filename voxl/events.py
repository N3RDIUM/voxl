from dataclasses import dataclass

from voxl.core.event_manager import Event
from voxl.types import KeyState


# TODO group these into separate sections, separate files if it gets really big
@dataclass
class DrawCall(Event):
    dt: float


@dataclass
class DebugDrawCall(Event): ...


@dataclass
class AssetsLoaded(Event):
    prefix: str


@dataclass
class QuadMeshCreated(Event):
    name: str


@dataclass
class QuadMeshUpdated(Event):
    name: str


@dataclass
class KeyEvent(Event):
    key_name: str
    state: KeyState


@dataclass
class MouseMoveEvent(Event):
    x: int
    y: int
