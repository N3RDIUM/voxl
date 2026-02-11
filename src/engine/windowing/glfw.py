from threading import Thread
from time import perf_counter
from typing import override

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

from src.engine import Core
from src.engine.constants import WINDOW_BACKEND_GLFW
from src.engine.default_config import (
    ENABLE_VSYNC as DEFAULT_ENABLE_VSYNC,
)
from src.engine.default_config import (
    SAMPLES as DEFAULT_SAMPLES,
)
from src.engine.default_config import (
    WINDOW_HEIGHT as DEFAULT_HEIGHT,
)
from src.engine.default_config import (
    WINDOW_WIDTH as DEFAULT_WIDTH,
)
from src.engine.events import (
    DebugDrawCall,
    DrawCall,
    KeyEvent,
    MouseMoveEvent,
    UpdateTick,
)
from src.engine.types import GlfwWindowPointer, KeyState

from .glfw_keymap import get_key_name
from .headless import Window, WindowConfig


class GlfwConfig(WindowConfig):
    """The glfw-specific window configuration TypedDict.
    Extends :py:class:`src.engine.windowing.headless.WindowConfig`.

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

    Inherits :py:class:`src.engine.windowing.headless.Window`.
    """

    window: GlfwWindowPointer
    update_thread: Thread

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

        # start update thread with shared context
        self.update_thread = Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        # imgui context
        imgui.create_context()
        self.imgui_impl: GlfwRenderer = GlfwRenderer(self.window)

        # Apply configuration options
        enable_vsync = self.glfw_config.get("vsync", DEFAULT_ENABLE_VSYNC)
        glfw.swap_interval(int(enable_vsync))

        glfw.window_hint(
            glfw.SAMPLES, self.glfw_config.get("samples", DEFAULT_SAMPLES)
        )

        # Key state handlers
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)

    def key_callback(
        self,
        window: GlfwWindowPointer,
        key: int,
        scancode: int,
        action: int,
        mods: int,
    ) -> None:
        _ = window, scancode, mods

        state = KeyState.RELEASE
        if action == glfw.PRESS:
            state = KeyState.PRESS
        elif action == glfw.RELEASE:
            state = KeyState.RELEASE
        elif action == glfw.REPEAT:
            state = KeyState.REPEAT

        self.core.event_manager().emit(
            KeyEvent(key_name=get_key_name(key), state=state)
        )

    def cursor_pos_callback(
        self, window: GlfwWindowPointer, xpos: int, ypos: int
    ) -> None:
        _ = window
        self.core.event_manager().emit(MouseMoveEvent(x=xpos, y=ypos))

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
            glfw.poll_events()

            self.core.event_manager().emit(DrawCall(dt=dt))

            self.imgui_impl.process_inputs()
            imgui.new_frame()
            self.core.event_manager().emit(DebugDrawCall(dt=dt))
            imgui.render()
            self.imgui_impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)
            dt = perf_counter() - t0

        glfw.terminate()
        self.logger.info("Window closed")

    @override
    def update_loop(self) -> None:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        shared_context: GlfwWindowPointer = glfw.create_window(
            1, 1, "Voxl Glfw Shared Context", None, self.window
        )
        glfw.make_context_current(shared_context)
        dt = 1 / 60

        while not glfw.window_should_close(self.window):
            t0 = perf_counter()
            glfw.poll_events()

            self.core.event_manager().emit(UpdateTick(dt=dt))

            glfw.swap_buffers(shared_context)
            glfw.poll_events()
            dt = perf_counter() - t0

    @override
    def request_mouse_lock(self, mode: bool) -> None:
        super().request_mouse_lock(mode)

        if mode:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            return

        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    @property
    @override
    def size(self) -> tuple[int, int]:
        """Tuple size of the window, in the format `(width, height)`

        Returns:
            (width, height)
        """

        return glfw.get_window_size(self.window)
