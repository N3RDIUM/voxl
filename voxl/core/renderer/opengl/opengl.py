import platform
from typing import override
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_TRUE,
    GL_DEPTH_TEST,
    GL_LESS,
    GL_DEPTH_CLAMP,
    GL_CULL_FACE,
    GL_BACK,
    glViewport,
    glClearColor,
    glClear,
    glEnable,
    glDisable,
    glDepthFunc,
    glCullFace,
)

from voxl.core import Core
from voxl.core.renderer.opengl.quad_mesh import OpenGLQuadMesh
from voxl.core.scene import SceneGraph
from voxl.events import DrawCall, AssetsLoaded, QuadMeshCreated, QuadMeshUpdated
from voxl.constants import (
    RENDER_BACKEND_OPENGL,
    WINDOW_BACKEND_GLFW,
    WINDOW_BACKEND_HEADLESS,
)
from voxl.core.renderer.renderer import Renderer, RendererConfig
from voxl.core.windowing.headless import Window
from .shader import OpenGLShader


class OpenGLConfig(RendererConfig):
    """The OpenGL-specific configuration TypedDict."""


default_config: OpenGLConfig = {"backend": RENDER_BACKEND_OPENGL}


class OpenGLRenderer(Renderer):
    """The OpenGL render backend implementation."""

    opengl_config: OpenGLConfig
    quad_mesh_shader: OpenGLShader | None
    quad_meshes: dict[str, OpenGLQuadMesh]

    def __init__(
        self,
        config: RendererConfig,
        window: Window,
        scene_graph: SceneGraph,
        core: Core,
    ):
        """Initialize OpenGL."""

        super().__init__(config, window, scene_graph, core)
        self.logger.info("Initializing OpenGL render backend")
        self.opengl_config = config.get("opengl", default_config)

        # quad mesh related stuff
        self.quad_mesh_shader = None
        self.quad_meshes = {}

        # window backend specific initialization
        window_backend = window.config.get("backend")
        if window_backend == WINDOW_BACKEND_GLFW:
            self._init_glfw()
        elif window_backend == WINDOW_BACKEND_HEADLESS:
            self._init_headless()
        else:
            self.logger.warning(f"Unsupported window backend {window_backend}")

        # register listener(s)
        event_manager = self.core.event_manager()
        event_manager.listen(AssetsLoaded, self.load_shaders)  # pyright:ignore[reportArgumentType]
        event_manager.listen(QuadMeshCreated, self.on_create_quad_mesh)  # pyright:ignore[reportArgumentType]
        event_manager.listen(QuadMeshUpdated, self.on_update_quad_mesh)  # pyright:ignore[reportArgumentType]

    def load_shaders(self, event: AssetsLoaded) -> None:
        if event.prefix != "voxl_":
            return

        self.quad_mesh_shader = OpenGLShader(
            "voxl_quad_mesh", self.core.asset_manager()
        )
        self.quad_mesh_shader.compile()

    def on_create_quad_mesh(self, event: QuadMeshCreated) -> None:
        new_mesh = OpenGLQuadMesh()
        self.quad_meshes[event.name] = new_mesh

    def on_update_quad_mesh(self, event: QuadMeshUpdated) -> None:
        updated_mesh = self.scene_graph.request_quad_mesh(event.name)
        self.quad_meshes[event.name].visible = updated_mesh.visible
        self.quad_meshes[event.name].set_data(updated_mesh.data)

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

        view, projection = self.core.camera().generate_mvp(self.window.size)
        self.quad_mesh_shader.set_uniform("view", view)
        self.quad_mesh_shader.set_uniform("projection", projection)

    @override
    def render(self, event: DrawCall) -> None:
        """Render the scene using OpenGL.

        This function is passed to the window's drawcall hooks, and the window
        calls it every frame during the mainloop.
        """
        _ = event.dt

        width, height = self.window.size
        glViewport(0, 0, width, height)
        glClearColor(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.quad_mesh_shader is None:
            return

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_CLAMP)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        self.quad_mesh_shader.use()
        self.set_shader_uniforms()
        for mesh in self.quad_meshes.values():
            if not mesh.visible:
                continue
            mesh.render()

        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_DEPTH_CLAMP)
