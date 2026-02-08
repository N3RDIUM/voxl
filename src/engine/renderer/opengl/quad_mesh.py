import ctypes

import numpy as np
import numpy.typing as npt
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_FLOAT,
    GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glBindBuffer,
    glDisableVertexAttribArray,
    glDrawArraysInstanced,
    glEnableVertexAttribArray,
    glVertexAttribDivisor,
    glVertexAttribPointer,
)
from typing_extensions import override

from src.engine import AssetManager
from src.engine.core import Core
from src.engine.scene.quad import Quad
from src.engine.scene.quad_mesh import QuadMesh

from .buffer import Buffer

Instance = np.dtype(
    [
        ("position", np.float32, 3),
        ("orientation", np.uint32),
        ("width", np.uint32),
        ("height", np.uint32),
        ("texture", np.float32),
    ]
)
type InstanceArray = npt.NDArray[np.void]


def quads_to_instances(
    quads: list[Quad], asset_manager: AssetManager
) -> np.ndarray:
    """Converts a given list of quads to an array of quad instance structs."""

    count = len(quads)
    instances = np.empty(count, dtype=Instance)

    for i, q in enumerate(quads):
        instances["position"][i] = q.position
        instances["orientation"][i] = np.uint32(q.orientation.value)
        instances["width"][i] = np.float32(q.width).view(np.uint32)
        instances["height"][i] = np.float32(q.height).view(np.uint32)
        instances["texture"][i] = float(asset_manager.texture_index(q.texture))

    return instances


class OpenGLQuadMesh(QuadMesh):
    """A drawable mesh of quads.

    Handles mesh modification with double-buffering, as well as binding, setting
    the necessary uniforms and rendering the mesh.

    TODO: Each mesh has a unique ID. An OpenGLQuadMesh in the renderer
    corresponds to a QuadMesh object. Then use the event pipeline to listen
    for updates.
    """

    buffers: list[Buffer]
    core: Core

    def __init__(self, core: Core) -> None:
        super().__init__()
        self.buffers = []
        self.core = core

    @override
    def set_data(self, data: list[Quad]) -> None:
        """Set the data used to render the mesh.

        Converts the given list of quads to instances using
        :py:func:`quads_to_instances`. Then creates a buffer, adds this data to
        it and appends it to the internal list of buffers.

        Currently, the mesh data is sent to the GPU immediately after calling
        this function. This may result in performance drops, will implement a
        scheduling system in the update function later.
        """

        # Don't do this, it'll duplicate the list of quads, and there's
        # literally no need to do that at this point.
        # super().set_data(data)

        # maybe make a texture_map dict instead of this.
        mesh_data = quads_to_instances(data, self.core.asset_manager())
        newbuf = Buffer(mesh_data)
        newbuf.send_to_gpu()
        self.buffers.append(newbuf)

    def render(self) -> None:
        """Render the mesh.

        Checks if any meshes are available to draw, binds them, sets up the
        necessary uniforms/attributes, sends the draw call, then cleans
        everything up.
        """

        if not self.buffers:
            return
        buffer = self.buffers[-1]

        glBindBuffer(GL_ARRAY_BUFFER, buffer.buffer)

        stride = buffer.data.strides[0]

        assert buffer.data.dtype.fields is not None
        offset_pos: int = buffer.data.dtype.fields["position"][1]
        offset_ori: int = buffer.data.dtype.fields["orientation"][1]
        offset_tex: int = buffer.data.dtype.fields["texture"][1]
        offset_wid: int = buffer.data.dtype.fields["width"][1]
        offset_hei: int = buffer.data.dtype.fields["height"][1]

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, False, stride, ctypes.c_void_p(offset_pos)
        )
        glVertexAttribDivisor(0, 1)

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1, 1, GL_UNSIGNED_INT, False, stride, ctypes.c_void_p(offset_ori)
        )
        glVertexAttribDivisor(1, 1)

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2, 1, GL_FLOAT, False, stride, ctypes.c_void_p(offset_tex)
        )
        glVertexAttribDivisor(2, 1)

        glEnableVertexAttribArray(3)
        glVertexAttribPointer(
            3, 1, GL_FLOAT, False, stride, ctypes.c_void_p(offset_wid)
        )
        glVertexAttribDivisor(3, 1)

        glEnableVertexAttribArray(4)
        glVertexAttribPointer(
            4, 1, GL_FLOAT, False, stride, ctypes.c_void_p(offset_hei)
        )
        glVertexAttribDivisor(4, 1)

        glDrawArraysInstanced(GL_TRIANGLES, 0, 6, len(buffer.data))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glDisableVertexAttribArray(4)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def update_buffers(self) -> None:
        """Double buffering implementation.

        Only keep two buffers, keep removing the rest, one by one.
        """

        if len(self.buffers) <= 2:
            return

        del self.buffers[0]
