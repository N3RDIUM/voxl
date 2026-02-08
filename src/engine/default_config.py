"""Sane default configuration options.
Keep these separated from the constants!
"""

# GlfwWindowConfig
ENABLE_VSYNC: bool = True
WINDOW_WIDTH: int = 854
WINDOW_HEIGHT: int = 480
SAMPLES: int = 1

# ComputeManagerConfig
POWER_PREFERENCE: str = "high-performance"

# CameraConfig
DEFAULT_FOV: float = 45.0
DEFAULT_FAR: float = 1.0
DEFAULT_NEAR: float = 1_000_000_000.0
