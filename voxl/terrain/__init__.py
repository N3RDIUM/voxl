"""Just render a single cube for now, nothing else."""

from voxl.core.scene.quad import Quad
from voxl.types import Orientation


def cube(position: tuple[int, int, int]) -> list[Quad]:
    top = Quad(
        position=position,
        orientation=Orientation.TOP,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    bottom = Quad(
        position=position,
        orientation=Orientation.BOTTOM,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    left = Quad(
        position=position,
        orientation=Orientation.LEFT,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    right = Quad(
        position=position,
        orientation=Orientation.RIGHT,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    front = Quad(
        position=position,
        orientation=Orientation.FRONT,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    back = Quad(
        position=position,
        orientation=Orientation.BACK,
        width=1,
        height=1,
        texture="voxl:kekw",
    )
    return [top, bottom, left, right, front, back]
