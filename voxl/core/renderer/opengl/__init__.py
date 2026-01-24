"""The OpenGL-based renderer."""

from .opengl import OpenGLRenderer, OpenGLConfig
from .buffer import Buffer
from .quad_mesh import QuadMesh
from .shader import OpenGLShader

__all__ = [
    "OpenGLRenderer",
    "OpenGLConfig",
    "Buffer",
    "QuadMesh",
    "OpenGLShader"
]
