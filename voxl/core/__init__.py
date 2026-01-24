"""Core functionality

This module provides core functionality like loggging and windowing. Currently
only those two, but a render backend is coming soon.
"""

from .core import Core
from . import compute
from . import windowing
from . import asset_manager

__all__ = ["Core", "compute", "windowing", "asset_manager"]
