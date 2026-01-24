import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    glGenBuffers,
    glBindBuffer,
    glBufferData,
    glBufferSubData,
    glDeleteBuffers,
    glFlush,
)


class Buffer:
    """Simple wrapper for OpenGL Array Buffers. Data stored is immutable."""

    data: np.ndarray
    buffer: int

    def __init__(self, data: np.ndarray) -> None:
        self.data = data
        self.buffer = glGenBuffers(1)

    def send_to_gpu(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.data.nbytes, self.data)
        glFlush()

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.buffer])
        del self.data
