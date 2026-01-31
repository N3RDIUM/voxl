"""Global Constants for Voxl.

This modules contains constants. Basically magic values but with names. At least
they're not magic values.
"""

from voxl.types import RenderBackend as RenderBackendType
from voxl.types import WindowBackend as WindowBackendType

# Window backends
WINDOW_BACKEND_HEADLESS: WindowBackendType = "headless"
WINDOW_BACKEND_GLFW: WindowBackendType = "glfw"

# Render backends
RENDER_BACKEND_NONE: RenderBackendType = "none"
RENDER_BACKEND_OPENGL: RenderBackendType = "opengl"
