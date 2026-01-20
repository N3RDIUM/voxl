import platform
from typing import override
from OpenGL.GL import (
    glViewport,
    glClearColor,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_TRUE,
)

from voxl.constants import (
    RENDER_BACKEND_OPENGL,
    WINDOW_BACKEND_GLFW,
    WINDOW_BACKEND_HEADLESS,
)
from .renderer import Renderer, RendererConfig
from voxl.core.windowing.headless import Window


class OpenGLConfig(RendererConfig):
    """The OpenGL-specific configuration TypedDict."""


default_config: OpenGLConfig = {"backend": RENDER_BACKEND_OPENGL}


class OpenGLRenderer(Renderer):
    """The OpenGL render backend implementation."""

    def __init__(self, config: RendererConfig, window: Window):
        """Initialize OpenGL."""

        super().__init__(config, window)
        self.logger.info("Initializing OpenGL render backend")
        self.opengl_config: OpenGLConfig = config.get("opengl", default_config)

        # window backend specific initialization
        window_backend = window.config.get("backend")
        if window_backend == WINDOW_BACKEND_GLFW:
            self._init_glfw()
        elif window_backend == WINDOW_BACKEND_HEADLESS:
            self._init_headless()
        else:
            self.logger.warning(f"Unsupported window backend {window_backend}")

        # other init
        ...

        window.register_hook("OpenGLRender", self.render)

    def _init_glfw(self):
        """Initialize OpenGL for the glfw backend.

        Sets the major and minor versions, and a platform-specific option
        for MacOS.
        """

        import glfw

        self.logger.info("Setting up glfw")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

        if platform.system() != "Darwin":
            return

        # make macos happy
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    def _init_headless(self):
        """Initialize OpenGL for the headless backend.

        Currently only logs a warning.
        """
        self.logger.warning("On headless backend")

    @override
    def render(self, dt: float) -> None:
        """Render the scene using OpenGL.

        This function is passed to the window's drawcall hooks, and the window
        calls it every frame during the mainloop.
        """
        width, height = self.window.size
        glViewport(0, 0, width, height)
        glClearColor(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT)
