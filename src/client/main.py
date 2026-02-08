"""Voxl client entry point"""

import imgui
from dependency_injector.wiring import Provide, inject

from src.client.di_containers import Voxl
from src.client.player import Player
from src.engine import AssetManager
from src.engine.events import DebugDrawCall
from src.engine.renderer.renderer import Renderer
from src.engine.scene import SceneGraph
from src.engine.windowing.headless import Window


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
    """The main entry point."""

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
