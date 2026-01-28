from typing import TypedDict
from logging import Logger, getLogger

from voxl.core import Core
from voxl.core.scene import SceneGraph
from voxl.events import DrawCall
from voxl.types import RenderBackend as RenderBackedType
from voxl.constants import RENDER_BACKEND_NONE
from voxl.core.windowing.headless import Window


class RendererConfig(TypedDict):
    """The renderer configuration TypedDict, as loaded from `config.yml`.

    Parameters:
        backend: one of {none, opengl}
    """

    backend: RenderBackedType


class Renderer:
    """Renderer base class, mainly for development/testing purposes.

    It also serves as a base `Renderer` class for the other renderers to build
    off of. Also implements the logging configuration.

    Attributes:
        config (RendererConfig): The renderer configuration TypedDict
        logger (Logger): Logger instance
    """

    config: RendererConfig
    window: Window
    scene_graph: SceneGraph
    core: Core
    logger: Logger

    def __init__(
        self,
        config: RendererConfig,
        window: Window,
        scene_graph: SceneGraph,
        core: Core,
    ) -> None:
        self.config = config
        self.window = window
        self.scene_graph = scene_graph
        self.core = core
        self.logger = getLogger("Renderer")

        if not config.get("backend"):
            self.logger.warning(
                "Renderer backend not configured. Please set `renderer.backend`"
                + " in `config.yml`."
            )

        if config.get("backend") == RENDER_BACKEND_NONE:
            self.logger.warning(
                "Running with the dummy renderer. Nothing will be drawn."
            )

        # register listeners
        self.core.event_manager().listen(DrawCall, self.render)  # pyright:ignore[reportArgumentType]

    def render(self, event: DrawCall) -> None:
        """Does nothing."""
        _ = event.dt
