from dataclasses import dataclass
from voxl.core.event_manager import Event


@dataclass
class DrawCall(Event):
    dt: float


@dataclass
class AssetsLoaded(Event):
    prefix: str
