"""Just render a single cube for now, nothing else."""

from voxl.core.scene.quad import Quad
from voxl.types import Orientation


def cube(position: tuple[int, int, int]) -> list[Quad]:
    top = Quad(
        position=position,
        orientation=Orientation.TOP,
        width=1,
        height=1,
        texture=0,
    )
    bottom = Quad(
        position=position,
        orientation=Orientation.BOTTOM,
        width=1,
        height=1,
        texture=0,
    )
    left = Quad(
        position=position,
        orientation=Orientation.LEFT,
        width=1,
        height=1,
        texture=0,
    )
    right = Quad(
        position=position,
        orientation=Orientation.RIGHT,
        width=1,
        height=1,
        texture=0,
    )
    front = Quad(
        position=position,
        orientation=Orientation.FRONT,
        width=1,
        height=1,
        texture=0,
    )
    back = Quad(
        position=position,
        orientation=Orientation.BACK,
        width=1,
        height=1,
        texture=0,
    )
    return [top, bottom, left, right, front, back]
