"""Module for the rendering system.

Backends are modular, and a dummy backend is also implemented for whatever
reason. The renderer backend can be easily configured through the `config.yml`
configuration file. For more windowing-related configuration options, see
:py:class:`src.engine.renderer.renderer.RendererConfig`.
"""

from .opengl import OpenGLConfig, OpenGLRenderer
from .renderer import Renderer, RendererConfig

__all__ = ["Renderer", "RendererConfig", "OpenGLRenderer", "OpenGLConfig"]
