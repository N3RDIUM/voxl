from .quad import Quad


class QuadMesh:
    """Simple quad mesh."""

    visible: bool
    data: list[Quad]
    # TODO AABB bounds to check for which meshes to actually draw.

    def __init__(self) -> None:
        self.visible = False
        self.data = []

    def set_data(self, data: list[Quad]) -> None:
        self.data = data
