import threading
from logging import Logger, getLogger
from typing import Callable, TypedDict

from src.engine import Core
from src.engine.constants import WINDOW_BACKEND_HEADLESS
from src.engine.events import DrawCall, UpdateTick
from src.engine.types import WindowBackend as WindowBackendType


class WindowConfig(TypedDict):
    """The window configuration TypedDict, as loaded from `config.yml`.

    Parameters:
        backend: one of {headless, glfw}
    """

    backend: (
        WindowBackendType  # TODO make this an enum and move here instead of
    )
    # contants.py.


# TODO move to types.py
type CallableHook = Callable[[float], None]


class Window:
    """Just a headless window instance, mainly for testing/development purposes.

    This also serves as the base `Window` class for other backends to build off
    of. Implements logging configuration (the `logger` parameter).

    Attributes:
        config (WindowConfig): The window configuration TypedDict
        logger (Logger): Logger instance
    """

    def __init__(self, config: WindowConfig, core: Core):
        self.config: WindowConfig = config
        self.core: Core = core
        self.logger: Logger = getLogger("Window")
        self.mouse_locked: bool = False

        if not config.get("backend"):
            self.logger.warning(
                "Window backend not configured. Please set `window.backend`"
                + " in `config.yml`."
            )

        if config.get("backend") == WINDOW_BACKEND_HEADLESS:
            self.update_thread: threading.Thread = threading.Thread(
                target=self.update_loop, daemon=True
            )
            self.update_thread.start()
            self.logger.warning(
                "Running with a headless window. No window will be displayed."
            )

    def mainloop(self) -> None:
        """A mainloop that does nothing. Forever. Until interrupted."""
        while True:
            self.core.event_manager().emit(DrawCall(dt=0.0))

    def request_mouse_lock(self, mode: bool) -> None:
        """Request the window to lock the mouse pointer.

        Args:
            mode: True is lock, False isn't.
        """

        self.mouse_locked = mode

    def update_loop(self) -> None:
        while True:
            self.core.event_manager().emit(UpdateTick(dt=0.0))

    @property
    def size(self) -> tuple[int, int]:
        """Tuple size of the window, in the format `(width, height)`

        Since this is a headless instance/dummy window, this function always
        returns (0, 0).

        Returns:
            (0, 0)
        """

        return 0, 0
