"""Utilities for easy usage of compute shaders in the engine."""

from typing_extensions import TypedDict
from logging import Logger, getLogger
from voxl.types import ComputeBindings

import wgpu
from wgpu.classes import (
    GPUBindGroup,
    GPUBuffer,
    GPUAdapter,
    GPUComputePassEncoder,
    GPUComputePipeline,
    GPUDevice,
)
from wgpu.structs import BindGroupEntry


class ComputeManagerConfig(TypedDict):
    """The compute manager configuration TypedDict."""


class ComputeManager:
    """Minimal compute shader API
    """
    config: ComputeManagerConfig
    adapter: GPUAdapter
    device: GPUDevice

    def __init__(self, config: ComputeManagerConfig) -> None:
        """TODO write docstrings once the thing is actually made.
        """
        self.config = config
        self.logger: Logger = getLogger("ComputeManager")

        self.logger.info("Initializing wgpu")
        self.adapter = wgpu.gpu.request_adapter_sync(
            power_preference="high-performance"
        )
        self.device = self.adapter.request_device_sync()

        self.dispatch_queue = []

    def run_compute_pass(self):
        # do n items from the queue
        pass

# TODO compute shader code as assets.
class ComputePipeline:
    shader: str
    bindings: ComputeBindings
    manager: ComputeManager
    pipeline: GPUComputePipeline

    def __init__(
        self,
        shader: str,
        entry_point: str,
        bindings: ComputeBindings,
        manager: ComputeManager,
    ) -> None:
        self.shader = shader
        self.bindings = bindings
        self.manager = manager

        device = manager.device
        self.pipeline = device.create_compute_pipeline(
            layout="auto",
            compute={"module": self.shader, "entry_point": entry_point},
        )

    def _build_groups(
        self,
        bindings: ComputeBindings
    ) -> dict[int, GPUBindGroup]:
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
        self, binding: dict[int, GPUBuffer]
    ) -> list[BindGroupEntry]:
        entries: list[BindGroupEntry] = []

        for entry in entries:
            entries.append({"binding": entry, "resource": binding[entry]})

        return entries

    def dispatch(
        self,
        pass_encoder: GPUComputePassEncoder,
        bindings: ComputeBindings,
        n_workgroups: tuple[int, int, int] = (1, 1, 1)
    ) -> None:
        pass_encoder.set_pipeline(self.pipeline)

        bind_groups: dict[int, GPUBindGroup]  = self._build_groups(bindings)
        for group_idx in bind_groups:
            pass_encoder.set_bind_group(
                group_idx,
                bind_groups[group_idx],
                dynamic_offsets_data=[],
                dynamic_offsets_data_start=0,
                dynamic_offsets_data_length=999999 # todo what?!
            )

        pass_encoder.dispatch_workgroups(*n_workgroups)

