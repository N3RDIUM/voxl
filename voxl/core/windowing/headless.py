from typing import Callable, TypedDict
from logging import Logger, getLogger

from voxl.types import WindowBackend as WindowBackendType
from voxl.constants import WINDOW_BACKEND_HEADLESS


class WindowConfig(TypedDict):
    """The window configuration TypedDict, as loaded from `config.yml`.

    Parameters:
        backend: one of {headless, glfw}
    """

    backend: WindowBackendType  # TODO make this an enum and move here instead of
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

    def __init__(self, config: WindowConfig):
        self.config: WindowConfig = config
        self.logger: Logger = getLogger("Window")

        self._drawcall_hooks: dict[str, CallableHook] = {}

        if not config.get("backend"):
            self.logger.warning(
                "Window backend not configured. Please set `window.backend`"
                + " in `config.yml`."
            )

        if config.get("backend") == WINDOW_BACKEND_HEADLESS:
            self.logger.warning(
                "Running with a headless window. No window will be displayed."
            )

    def register_hook(
        self,
        name: str,
        hook: CallableHook,
    ) -> None:
        self._drawcall_hooks[name] = hook

    def call_hooks(self, dt: float) -> None:
        hooks = self._drawcall_hooks
        for hook in hooks.values():
            hook(dt)

    def mainloop(self) -> None:
        """A mainloop that does nothing. Forever. Until interrupted."""
        dt = 0.0

        while True:
            self.call_hooks(dt)

    @property
    def size(self) -> tuple[int, int]:
        """Tuple size of the window, in the format `(width, height)`

        Since this is a headless instance/dummy window, this function always
        returns (0, 0).

        Returns:
            (0, 0)
        """

        return 0, 0
