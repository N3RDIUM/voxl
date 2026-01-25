"""Core functionality

This module provides core functionality: compute shaders, windowing, asset
management, logging, rendering, and a simple camera/MVP.
"""

from .core import Core
from . import compute
from . import windowing
from . import renderer
from . import asset_manager
from . import camera

__all__ = [
    "Core",
    "compute",
    "windowing",
    "renderer",
    "asset_manager",
    "camera",
]
