from typing import override
from time import perf_counter
import glfw

from voxl.core import Core
from voxl.events import DrawCall
from voxl.types import GlfwWindowPointer

from .headless import Window, WindowConfig
from voxl.constants import WINDOW_BACKEND_GLFW
from voxl.default_config import (
    ENABLE_VSYNC as DEFAULT_ENABLE_VSYNC,
    WINDOW_WIDTH as DEFAULT_WIDTH,
    WINDOW_HEIGHT as DEFAULT_HEIGHT,
    SAMPLES as DEFAULT_SAMPLES,
)


class GlfwConfig(WindowConfig):
    """The glfw-specific window configuration TypedDict.
    Extends :py:class:`voxl.core.windowing.headless.WindowConfig`.

    Parameters:
        width (int): the default width of the window
        height (int): the default height of the window
        vsync (bool): whether to enable vsync
        samples (int): the number of samples for anti-aliasing
    """

    width: int
    height: int
    vsync: bool
    samples: int


default_config: GlfwConfig = {
    "backend": WINDOW_BACKEND_GLFW,
    "width": DEFAULT_WIDTH,
    "height": DEFAULT_HEIGHT,
    "vsync": DEFAULT_ENABLE_VSYNC,
    "samples": DEFAULT_SAMPLES,
}


class GlfwWindow(Window):
    """Wrapper for easily handling glfw windows.

    Inherits :py:class:`voxl.core.windowing.headless.Window`.
    """

    window: GlfwWindowPointer

    def __init__(self, config: WindowConfig, core: Core) -> None:
        """Initialize the glfw window and configure it.

        This constructor is responsible for initializing the glfw backend,
        creating the context and making it current, and applying window
        configuration options in that order.
        """

        super().__init__(config, core)
        self.logger.info("Initializing glfw backend")
        assert config["backend"] == WINDOW_BACKEND_GLFW
        self.glfw_config: GlfwConfig = config.get("glfw", default_config)

        if not glfw.init():
            raise Exception("Could not initialize glfw!")

        self.logger.info("Creating glfw window")
        self.window = glfw.create_window(
            self.glfw_config.get("width", DEFAULT_WIDTH),
            self.glfw_config.get("height", DEFAULT_HEIGHT),
            "Voxl",
            None,
            None,
        )
        if not self.window:
            glfw.terminate()
            raise Exception("Could not create glfw window")
        glfw.make_context_current(self.window)

        # Apply configuration options
        enable_vsync = self.glfw_config.get("vsync", DEFAULT_ENABLE_VSYNC)
        glfw.swap_interval(int(enable_vsync))

        glfw.window_hint(
            glfw.SAMPLES, self.glfw_config.get("samples", DEFAULT_SAMPLES)
        )

        # TODO key callbacks (keyboard handler?)
        ...

    @override
    def mainloop(self) -> None:
        """Start the mainloop.

        Currently only draws a black window, since the render backend isn't
        implemented yet.
        """
        dt = 1 / 60

        self.logger.info("Starting mainloop")
        while not glfw.window_should_close(self.window):
            t0 = perf_counter()

            self.core.event_manager().emit(DrawCall(dt=dt))

            glfw.swap_buffers(self.window)
            glfw.poll_events()
            dt = perf_counter() - t0

        glfw.terminate()
        self.logger.info("Window closed")

    @property
    @override
    def size(self) -> tuple[int, int]:
        """Tuple size of the window, in the format `(width, height)`

        Returns:
            (width, height)
        """

        return glfw.get_window_size(self.window)
