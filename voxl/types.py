"""Type alias declarations. Currently just one tho.

This project takes type safety seriously. That's why.
"""

from typing import Literal
from wgpu import GPUBuffer

# core.windowing
type WindowBackend = Literal["headless", "glfw"]
type GlfwWindowPointer = int

# core.renderer
type RenderBackend = Literal["none", "opengl"]

# core.compute
type ComputeBindings = dict[int, dict[int, GPUBuffer]] # TODO docstring
