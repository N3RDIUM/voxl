"""Module for the rendering system.

Backends are modular, and a dummy backend is also implemented for whatever
reason. The renderer backend can be easily configured through the `config.yml`
configuration file. For more windowing-related configuration options, see
:py:class:`voxl.core.renderer.renderer.RendererConfig`.
"""

from .renderer import Renderer, RendererConfig
from .opengl import OpenGLRenderer, OpenGLConfig

__all__ = ["Renderer", "RendererConfig", "OpenGLRenderer", "OpenGLConfig"]
