"""Core functionality

This module provides core functionality like loggging and windowing. Currently
only those two, but a render backend is coming soon.
"""

from .core import Core
from . import windowing

__all__ = ["Core", "windowing"]
