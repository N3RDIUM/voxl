import math

from src.engine import EventManager
from src.engine.events import DrawCall, KeyEvent, MouseMoveEvent
from src.engine.types import KeyState
from src.engine.windowing.headless import Window


class Player:
    window: Window
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    cursor_pos: tuple[float, float]
    keys: dict[str, bool]

    def __init__(self, window: Window) -> None:
        self.window = window
        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.cursor_pos = (0, 0)
        self.keys = {}

        window.request_mouse_lock(True)

        event_manager: EventManager = window.core.event_manager()
        event_manager.listen(KeyEvent, self.on_key)  # pyright:ignore[reportArgumentType]
        event_manager.listen(MouseMoveEvent, self.on_mouse_move)  # pyright:ignore[reportArgumentType]
        event_manager.listen(DrawCall, self.update)  # pyright:ignore[reportArgumentType]

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

        # TODO configurable mouse sensitivity
        dx = event.x - self.cursor_pos[0]
        dy = event.y - self.cursor_pos[1]

        self.rotation = (
            max(-90, min(90, self.rotation[0] + dy)),
            (self.rotation[1] + dx) % 360,
            self.rotation[2],
        )

        self.cursor_pos = (event.x, event.y)

    def update(self, event: DrawCall) -> None:
        if not self.window.mouse_locked:
            return

        dt = event.dt
        speed = 5.0

        yaw = math.radians(self.rotation[1])
        forward_x = math.sin(yaw)
        forward_z = -math.cos(yaw)
        right_x = math.cos(yaw)
        right_z = math.sin(yaw)

        dx, dy, dz = 0, 0, 0
        if self.keys.get("W"):
            dx -= forward_x * speed * dt
            dz -= forward_z * speed * dt
        if self.keys.get("S"):
            dx += forward_x * speed * dt
            dz += forward_z * speed * dt
        if self.keys.get("D"):
            dx -= right_x * speed * dt
            dz -= right_z * speed * dt
        if self.keys.get("A"):
            dx += right_x * speed * dt
            dz += right_z * speed * dt

        if self.keys.get("SPACE"):
            dy -= speed * dt
        if self.keys.get("LEFT_SHIFT"):
            dy += speed * dt

        self.position = (
            self.position[0] + dx,
            self.position[1] + dy,
            self.position[2] + dz,
        )

        camera = self.window.core.camera()
        camera.position = self.position
        camera.rotation = self.rotation
