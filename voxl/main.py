"""Voxl entry point

Initializes everything, loads the configuration from `config.yml` in the cwd,
handles program startup and post-termination cleanups.
"""

from dependency_injector.wiring import Provide, inject

from voxl.core import AssetManager
from voxl.core.renderer.renderer import Renderer
from voxl.core.scene import Quad, QuadMesh, SceneGraph
from voxl.core.windowing.headless import Window
from voxl.di_containers import Voxl
from voxl.events import DrawCall, KeyEvent, MouseMoveEvent
from voxl.player import Player
from voxl.terrain import cube


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
    data: list[Quad] = []
    for x in range(16):
        for y in range(16):
            for z in range(16):
                data.extend(cube((x, y, z - 12)))
    mesh.set_data(data)
    mesh.visible = True

    # changes to a quad mesh won't be reflected unless this is called:
    scene_graph.update_quad_mesh("example")

    # player
    player = Player(window)
    event_manager = (
        window.core.event_manager()
    )  # TODO: Maybe let the player handle these
    event_manager.listen(KeyEvent, player.on_key)  # pyright:ignore[reportArgumentType]
    event_manager.listen(MouseMoveEvent, player.on_mouse_move)  # pyright:ignore[reportArgumentType]
    event_manager.listen(DrawCall, player.update)  # pyright:ignore[reportArgumentType]

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
