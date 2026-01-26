from typing import TypedDict
from logging import Logger, getLogger

from voxl.core import AssetManager, Camera
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
    asset_manager: AssetManager
    camera: Camera
    logger: Logger

    def __init__(
        self,
        config: RendererConfig,
        window: Window,
        asset_manager: AssetManager,
        camera: Camera,
    ) -> None:
        self.config = config
        self.window = window
        self.asset_manager = asset_manager
        self.camera = camera
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

    def render(self, dt: float) -> None:
        """Does nothing."""
        _ = dt

    def request_quad_mesh(self, uid: str) -> None:  # -> quadmesh base, actually
        """Request the creation of a quad mesh."""

        # TODO: the OpenGLQuadMesh should inherit from the QuadMesh in core.scene

        _ = uid
        raise NotImplementedError
