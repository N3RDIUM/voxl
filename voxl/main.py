"""Voxl entry point

Initializes everything, loads the configuration from `config.yml` in the cwd,
handles program startup and post-termination cleanups.
"""

from dependency_injector.wiring import Provide, inject

from voxl.core import AssetManager
from voxl.core.scene import QuadMesh, SceneGraph
from voxl.terrain import cube
from voxl.core.windowing.headless import Window
from voxl.core.renderer.renderer import Renderer
from voxl.di_containers import Voxl


@inject
def main(
    asset_manager: AssetManager = Provide[Voxl.core.asset_manager],  # pyright:ignore[reportUnknownMemberType]
    scene_graph: SceneGraph = Provide[Voxl.scene_graph],
    renderer: Renderer = Provide[Voxl.renderer],
    window: Window = Provide[Voxl.window],
) -> None:
    """The main entry point.

    Starts the application mainloop and handles after-close cleanup.
    """

    asset_manager.load_assets("./assets/", "voxl_")
    _ = renderer

    mesh: QuadMesh = scene_graph.request_quad_mesh("example", create=True)
    mesh.visible = True
    mesh.set_data(cube((0, 0, -4)))

    # changes to a quad mesh won't be reflected unless this is called:
    scene_graph.update_quad_mesh("example")

    try:
        window.mainloop()
    except KeyboardInterrupt:
        ...

    # TODO cleanup


if __name__ == "__main__":
    app = Voxl()

    app.config.from_yaml("config.yml")

    core = app.core()
    core.logging()

    app.wire(modules=[__name__])
    main()
