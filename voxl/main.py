"""Voxl entry point

Initializes everything, loads the configuration from `config.yml` in the cwd,
handles program startup and post-termination cleanups.
"""

import imgui
from dependency_injector.wiring import Provide, inject

from voxl.core import AssetManager
from voxl.core.events import DebugDrawCall
from voxl.core.renderer.renderer import Renderer
from voxl.core.scene import SceneGraph
from voxl.core.windowing.headless import Window
from voxl.di_containers import Voxl
from voxl.player import Player


def fps_meter(event: DebugDrawCall):
    dt = event.dt
    fps = int(1 / dt)

    imgui.begin("Performance")
    imgui.text(f"{fps} FPS")
    imgui.end()


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

    asset_manager.load_assets("./assets/", "voxl")
    _ = renderer, scene_graph

    # player
    _ = Player(window)

    # hud
    window.core.event_manager().listen(DebugDrawCall, fps_meter)  # pyright:ignore[reportArgumentType]

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
