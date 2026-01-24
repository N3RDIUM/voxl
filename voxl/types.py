"""Type alias declarations all go here."""

from typing import Literal
from enum import Enum
from wgpu import GPUBuffer

# core.windowing
type WindowBackend = Literal["headless", "glfw"]
type GlfwWindowPointer = int

# core.renderer
type RenderBackend = Literal["none", "opengl"]


# core.renderer.quad
class Orientation(Enum):
    """Enum for the orientation of a quad in 3d space.

    Attributes:
        TOP
        BOTTOM
        LEFT
        RIGHT
        FRONT
        BACK
    """

    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    FRONT = 4
    BACK = 5


# core.compute
type ComputeBindings = dict[int, dict[int, GPUBuffer]]
"""Representation of buffer binding layouts.

The outer layer of dictionaries represents the bind groups. The inner layer
corresponds to the buffers themselves.

Example:

    {
        0: {  # Bind group 0
            0: buffer0,  # @group(0) @bidning(0)
            1: buffer1   # @group(0) @binding(1)
        },
        1: {  # Bind group 1
            0: buffer2,  # @group(1) @binding(0)
            1: buffer3   # @group(1) @binding(1)
        }  # et cetra
    }

"""
