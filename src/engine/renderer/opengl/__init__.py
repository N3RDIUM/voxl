"""The OpenGL-based renderer."""

from .buffer import Buffer
from .opengl import OpenGLConfig, OpenGLRenderer
from .quad_mesh import OpenGLQuadMesh
from .shader import OpenGLShader

__all__ = [
    "OpenGLRenderer",
    "OpenGLConfig",
    "Buffer",
    "OpenGLQuadMesh",
    "OpenGLShader",
]
