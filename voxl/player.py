from voxl.core.windowing.headless import Window
from voxl.events import DrawCall, KeyEvent, MouseMoveEvent
from voxl.types import KeyState


class Player:
    window: Window
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    cursor_pos: tuple[int, int]
    keys: dict[str, bool]

    def __init__(self, window: Window) -> None:
        self.window = window
        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.cursor_pos = (0, 0)
        self.keys = {}

        window.request_mouse_lock(True)

    def on_key(self, event: KeyEvent) -> None:
        self.keys[event.key_name] = event.state != KeyState.RELEASE

        if event.state != KeyState.PRESS:
            return

        if event.key_name == "L":
            self.window.request_mouse_lock(True)
        elif event.key_name == "ESCAPE":
            self.window.request_mouse_lock(False)

    def on_mouse_move(self, event: MouseMoveEvent) -> None:
        if not self.window.mouse_locked:
            return

        dx = event.x - self.cursor_pos[0]
        dy = event.y - self.cursor_pos[1]

        self.rotation = (
            self.rotation[0] + dy,
            self.rotation[1] + dx,
            self.rotation[2],
        )

        self.cursor_pos = (event.x, event.y)

    def update(self, event: DrawCall) -> None:
        _ = event

        camera = self.window.core.camera()
        camera.rotation = self.rotation
