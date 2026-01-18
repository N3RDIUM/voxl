"""Type alias declarations. Currently just one tho.

This project takes type safety seriously. That's why.
"""

from typing import Literal

type WindowBackend = Literal["headless", "glfw"]
type RenderBackend = Literal["none", "opengl"]
