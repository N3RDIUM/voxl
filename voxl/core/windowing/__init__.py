"""Module for the windowing system.

Backends are modular, and a `headless` window is also implemented for whatever
reason. The window backend can be easily configured through the `config.yml`
configuration file. For more windowing-related configuration options, see
:py:class:`voxl.core.windowing.headless.WindowConfig`
"""

from .headless import Window, WindowConfig
from .glfw import GlfwWindow, GlfwConfig

__all__ = ["Window", "WindowConfig", "GlfwWindow", "GlfwConfig"]
