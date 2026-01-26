"""Core functionality

This module provides core functionality: compute shaders, windowing, asset
management, logging, evenr management, rendering, and a simple camera/MVP.
"""

from .asset_manager import AssetManager, AssetManagerConfig
from .camera import Camera, CameraConfig
from .compute import ComputeManager, ComputePipeline, ComputeManagerConfig
from .core import Core
from .event_manager import EventManager, Event

__all__ = [
    "AssetManager",
    "AssetManagerConfig",
    "Camera",
    "CameraConfig",
    "ComputeManager",
    "ComputePipeline",
    "ComputeManagerConfig",
    "Core",
    "EventManager",
    "Event",
]
