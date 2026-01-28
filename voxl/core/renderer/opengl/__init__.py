"""The OpenGL-based renderer."""

from .opengl import OpenGLRenderer, OpenGLConfig
from .buffer import Buffer
from .quad_mesh import OpenGLQuadMesh
from .shader import OpenGLShader

__all__ = [
    "OpenGLRenderer",
    "OpenGLConfig",
    "Buffer",
    "OpenGLQuadMesh",
    "OpenGLShader",
]
