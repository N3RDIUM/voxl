"""Core functionality

This module provides core functionality: compute shaders, windowing, asset
management, logging, rendering, and a simple camera/MVP.
"""

from .asset_manager import AssetManager, AssetManagerConfig
from .camera import Camera, CameraConfig
from .compute import ComputeManager, ComputePipeline, ComputeManagerConfig
from .core import Core
from . import windowing
from . import renderer

__all__ = [
    "AssetManager",
    "AssetManagerConfig",
    "Camera",
    "CameraConfig",
    "ComputeManager",
    "ComputePipeline",
    "ComputeManagerConfig",
    "Core",
    "windowing",
    "renderer",
]
