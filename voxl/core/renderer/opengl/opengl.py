import platform
from typing import override
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_TRUE,
    GL_DEPTH_TEST,
    GL_LESS,
    GL_DEPTH_CLAMP,
    glViewport,
    glClearColor,
    glClear,
    glEnable,
    glDisable,
    glDepthFunc,
)

from voxl.core import AssetManager, Camera
from voxl.constants import (
    RENDER_BACKEND_OPENGL,
    WINDOW_BACKEND_GLFW,
    WINDOW_BACKEND_HEADLESS,
)
from voxl.core.renderer.renderer import Renderer, RendererConfig
from voxl.core.windowing.headless import Window
from voxl.types import Orientation
from .shader import OpenGLShader
from .quad_mesh import QuadMesh
from voxl.core.renderer.quad import Quad
import random


class OpenGLConfig(RendererConfig):
    """The OpenGL-specific configuration TypedDict."""


default_config: OpenGLConfig = {"backend": RENDER_BACKEND_OPENGL}


class OpenGLRenderer(Renderer):
    """The OpenGL render backend implementation."""

    opengl_config: OpenGLConfig
    quad_mesh_shader: OpenGLShader | None

    def __init__(
        self,
        config: RendererConfig,
        window: Window,
        asset_manager: AssetManager,
        camera: Camera,
    ):
        """Initialize OpenGL."""

        super().__init__(config, window, asset_manager, camera)
        self.logger.info("Initializing OpenGL render backend")
        self.opengl_config = config.get("opengl", default_config)
        self.quad_mesh_shader = None

        # window backend specific initialization
        window_backend = window.config.get("backend")
        if window_backend == WINDOW_BACKEND_GLFW:
            self._init_glfw()
        elif window_backend == WINDOW_BACKEND_HEADLESS:
            self._init_headless()
        else:
            self.logger.warning(f"Unsupported window backend {window_backend}")

        # meshmeshmeshmeshmeshmeshmesh
        self.mesh: QuadMesh = QuadMesh()
        data = []
        for _ in range(16384):
            data.append(
                Quad(
                    position=(
                        random.randint(-42, 42),
                        random.randint(-42, 42),
                        random.randint(-42, 42),
                    ),
                    orientation=random.choice(
                        [
                            Orientation.TOP,
                            Orientation.BOTTOM,
                            Orientation.LEFT,
                            Orientation.RIGHT,
                            Orientation.FRONT,
                            Orientation.BACK,
                        ]
                    ),
                    width=1,
                    height=1,
                    texture=0,
                )
            )
        self.mesh.set_data(data)

        # register hooks
        asset_manager.register_hook(
            "OpenGLLoadShaders", "voxl_", self.load_shaders
        )
        window.register_hook("OpenGLRender", self.render)

    def load_shaders(self):
        self.quad_mesh_shader = OpenGLShader(
            "voxl_quad_mesh", self.asset_manager
        )
        self.quad_mesh_shader.compile()

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

    def set_shader_uniforms(
        self,
    ) -> None:  # TODO DI instead of arg-passing the Camera around
        if self.quad_mesh_shader is None:
            return

        view, projection = self.camera.generate_mvp(self.window.size)
        self.quad_mesh_shader.set_uniform("view", view)
        self.quad_mesh_shader.set_uniform("projection", projection)

    @override
    def render(self, dt: float) -> None:
        """Render the scene using OpenGL.

        This function is passed to the window's drawcall hooks, and the window
        calls it every frame during the mainloop.
        """

        width, height = self.window.size
        glViewport(0, 0, width, height)
        glClearColor(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_CLAMP)

        if self.quad_mesh_shader is None:
            return

        self.quad_mesh_shader.use()
        self.set_shader_uniforms()
        self.mesh.render()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_DEPTH_CLAMP)

        _ = dt
