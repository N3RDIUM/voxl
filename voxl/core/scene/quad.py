from dataclasses import dataclass
from voxl.types import Orientation


@dataclass
class Quad:
    """Representation of an axis-aligned quad in 3-dimensional space.

    Attributes:
        position: Tuple of floats, position in 3d space.
        orientation: Axis-aligned orientation. See
            :py:class:`voxl.types.Orientation` for more.
        width: Width of the quad
        height: Height of the quad
        texture: Texture index, currently unused.
    """

    position: tuple[float, float, float]
    orientation: Orientation
    width: float
    height: float
    texture: int
