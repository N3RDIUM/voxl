"""Minimal utilities providing compute shaders."""

# TODO improve docstrings in this file.

from time import perf_counter
import numpy as np
from typing_extensions import TypedDict
from logging import Logger, getLogger
from voxl.types import ComputeBindings
from voxl.default_config import POWER_PREFERENCE as DEFAULT_POWER_PREFERENCE

import wgpu
from wgpu.classes import (
    GPUBindGroup,
    GPUBuffer,
    GPUAdapter,
    GPUComputePassEncoder,
    GPUComputePipeline,
    GPUDevice,
    GPUShaderModule,
)
from wgpu.structs import BindGroupEntry
from wgpu.flags import BufferUsage


class ComputeManagerConfig(TypedDict):
    """The compute manager configuration TypedDict."""

    power_preference: str


class DispatchDict(TypedDict):
    pipeline: ComputePipeline
    bindings: ComputeBindings
    n_workgroups: tuple[int, int, int]


class ComputeManager:
    """Minimal wgpu compute manager."""

    config: ComputeManagerConfig
    adapter: GPUAdapter
    device: GPUDevice
    dispatch_queue: list[DispatchDict]

    def __init__(self, config: ComputeManagerConfig) -> None:
        """Initialize the compute manager."""

        self.config = config
        self.logger: Logger = getLogger("ComputeManager")

        t0 = perf_counter()
        self.logger.info("Initializing wgpu")
        self.adapter = wgpu.gpu.request_adapter_sync(
            power_preference=self.config.get(
                "power_preference", DEFAULT_POWER_PREFERENCE
            )
        )
        self.device = self.adapter.request_device_sync()

        # this step is relatively slow. log time elapsed.
        self.logger.info(f"wgpu init took {perf_counter() - t0} sec")

        self.dispatch_queue = []  # TODO TypedDict 'ComputeDispatch'

    def compute_pass(self) -> None:
        """Run a single compute pass.

        Handles command encoders, does the compute pass and dispatches items
        from the dispatch queue.
        """

        encoder = self.device.create_command_encoder()
        pass_encoder = encoder.begin_compute_pass()

        for item in self.dispatch_queue:
            pipeline = item["pipeline"]
            bindings = item["bindings"]
            n_workgroups = item["n_workgroups"]
            pipeline.dispatch(pass_encoder, bindings, n_workgroups)

        pass_encoder.end()
        self.device.queue.submit([encoder.finish()])

    def enqueue(
        self,
        pipeline: ComputePipeline,
        bindings: ComputeBindings,
        n_workgroups: tuple[int, int, int],
    ) -> None:
        """Enqueue a compute task.

        Stores the kwargs (apart from pipeline) in the dispatch queue. The
        kwargs other than pipeline are passed straight to pipeline.dispatch().
        For more info, see
        :py:meth:`voxl.core.compute.ComputePipeline.dispatch`.

        Args:
            pipeline (ComputePipeline): The compute pipeline to use.
            bindings: the buffer bindings to use.
            n_workgroups: number of workgroups to dispatch.
        """

        self.dispatch_queue.append(
            {
                "pipeline": pipeline,
                "bindings": bindings,
                "n_workgroups": n_workgroups,
            }
        )

    def buffer_from_np(
        self,
        data: np.ndarray,
        usage: int = BufferUsage.STORAGE
        | BufferUsage.COPY_SRC
        | BufferUsage.COPY_DST,
    ) -> GPUBuffer:
        """Create a GPUBuffer from a given numpy array."""

        return self.device.create_buffer_with_data(
            data=data.tobytes(), usage=usage
        )

    def readback(
        self, buffer: GPUBuffer, nbytes: int, dtype: str
    ) -> np.ndarray:
        """Read back the results of the computation into a numpy array."""

        readback_buffer = self.device.create_buffer(
            size=nbytes,
            usage=BufferUsage.COPY_DST | BufferUsage.MAP_READ,
        )

        encoder = self.device.create_command_encoder()
        encoder.copy_buffer_to_buffer(buffer, 0, readback_buffer, 0, nbytes)
        self.device.queue.submit([encoder.finish()])

        result = self.device.queue.read_buffer(buffer)
        return np.frombuffer(result, dtype=dtype)


class ComputePipeline:
    """Handles wgpu compute pipeline creation for a compute shader."""

    shader: str
    manager: ComputeManager
    pipeline: GPUComputePipeline
    module: GPUShaderModule

    def __init__(
        self,
        shader: str,
        entry_point: str,
        manager: ComputeManager,
    ) -> None:
        """Compiles the shader module and creates a wgpu compute pipeline."""

        self.shader = shader
        self.manager = manager

        device = manager.device
        self.module = device.create_shader_module(code=shader)
        self.pipeline = device.create_compute_pipeline(
            layout="auto",
            compute={"module": self.module, "entry_point": entry_point},
        )

    def _build_groups(
        self, bindings: ComputeBindings
    ) -> dict[int, GPUBindGroup]:
        """Convert the simplified binding format into a wgpu-compatible struct.

        Args:
            bindings (ComputeBindings): dictionary of bindings. See
                :py:data:`voxl.types.ComputeBindings` for more.
        """

        groups: dict[int, GPUBindGroup] = {}

        for group_id in bindings:
            layout = self.pipeline.get_bind_group_layout(group_id)
            entries = self._build_group_entries(bindings[group_id])
            group = self.manager.device.create_bind_group(
                layout=layout,
                entries=entries,
            )
            groups[group_id] = group

        return groups

    def _build_group_entries(
        self, group: dict[int, GPUBuffer]
    ) -> list[BindGroupEntry]:
        """Build the buffer binding entries for a given bind group."""

        entries: list[BindGroupEntry] = []

        for buffer_idx in group:
            entries.append(
                {"binding": buffer_idx, "resource": group[buffer_idx]}
            )

        return entries

    def dispatch(
        self,
        pass_encoder: GPUComputePassEncoder,
        bindings: ComputeBindings,
        n_workgroups: tuple[int, int, int] = (1, 1, 1),
    ) -> None:
        """Dispatch the pipeline with the given data and n_workgroups

        Sets the pipeline to self, handles bind groups, and dispatches the
        pipeline to the pass encoder provided by
        :py:meth:`voxl.core.compute.ComputeManager.compute_pass`

        Args:
            pass_encoder: a compute pass encoder object.
            bindings: the buffer bindings to use. See
                :py:data:`voxl.types.ComputeBindings` for more.
            n_workgroups: number of workgroups to dispatch.
        """

        pass_encoder.set_pipeline(self.pipeline)

        bind_groups: dict[int, GPUBindGroup] = self._build_groups(bindings)
        for group_idx in bind_groups:
            pass_encoder.set_bind_group(
                group_idx,
                bind_groups[group_idx],
            )

        pass_encoder.dispatch_workgroups(*n_workgroups)
