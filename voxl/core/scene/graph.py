"""Scene graph.

Todo:
    * Instead of distinguishing between types of scene objects, make a base node
    * The camera should be a child of the scene graph. The scene graph will tell
    the renderer about the currently active camera and it will handle the rest
    accordingly.
"""

from voxl.core.core import Core
from voxl.core.events import QuadMeshCreated, QuadMeshUpdated

from .quad_mesh import QuadMesh


class SceneGraph:
    core: Core
    quad_meshes: dict[str, QuadMesh]

    def __init__(self, core: Core):
        self.core = core
        self.quad_meshes = {}

    def request_quad_mesh(self, name: str, create: bool = False):
        if self.quad_meshes.get(name):
            return self.quad_meshes[name]

        if not create:
            raise RuntimeError(
                f"Requested a quad mesh '{name}' which doesn't exist!"
            )

        new_mesh: QuadMesh = QuadMesh()
        self.quad_meshes[name] = new_mesh
        self.core.event_manager().emit(QuadMeshCreated(name=name))
        return new_mesh

    def update_quad_mesh(self, name: str):
        if not self.quad_meshes.get(name):
            raise RuntimeError(
                f"Tried to update a quad mesh '{name}' which doesn't exist!"
            )

        self.core.event_manager().emit(QuadMeshUpdated(name=name))
