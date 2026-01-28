from dataclasses import dataclass
from voxl.core.event_manager import Event


# TODO group these into separate sections, separate files if it gets really big
@dataclass
class DrawCall(Event):
    dt: float


@dataclass
class AssetsLoaded(Event):
    prefix: str


@dataclass
class QuadMeshCreated(Event):
    name: str


@dataclass
class QuadMeshUpdated(Event):
    name: str
