from collections.abc import Sequence
from typing import TypedDict
from wgpu.enums import FeatureNameEnum
from wgpu.structs import BindGroupEntry, QueueDescriptorStruct

class GPUCommandBuffer: ...

class GPUComputePassEncoder:
    def set_pipeline(self, pipeline: GPUComputePipeline) -> None: ...
    def set_bind_group(
        self,
        index: int,
        group: GPUBindGroup,
        dynamic_offsets_data: Sequence[int] = [],
        dynamic_offsets_data_start: int | None = None,
        dynamic_offsets_data_length: int | None = None,
    ) -> None: ...
    def dispatch_workgroups(
        self,
        workgroup_count_x: int | None = None,
        workgroup_count_y: int = 1,
        workgroup_count_z: int = 1,
    ) -> None: ...
    def end(self) -> None: ...

class GPUCommandEncoder:
    def begin_compute_pass(self) -> GPUComputePassEncoder: ...
    def finish(self) -> GPUCommandBuffer: ...
    def copy_buffer_to_buffer(
        self,
        source: GPUBuffer | None = None,
        source_offset: int | None = None,
        destination: GPUBuffer | None = None,
        destination_offset: int | None = None,
        size: int | None = None,
    ) -> None: ...

class GPUQueue:
    def submit(self, command_buffers: Sequence[GPUCommandBuffer]) -> None: ...
    def read_buffer(self, buffer: GPUBuffer) -> memoryview: ...

class GPUBuffer: ...
class GPUShaderModule: ...
class GPUBindGroup: ...
class GPUBindGroupLayout: ...

class GPUComputePipeline:
    def get_bind_group_layout(self, index: int) -> GPUBindGroupLayout: ...

class ComputeDict(TypedDict):
    module: GPUShaderModule
    entry_point: str

class GPUDevice:
    queue: GPUQueue
    def create_command_encoder(self) -> GPUCommandEncoder: ...
    def create_buffer(self, size: int, usage: int) -> GPUBuffer: ...
    def create_buffer_with_data(self, data: bytes, usage: int) -> GPUBuffer: ...
    def create_shader_module(
        self,
        code: str,
    ) -> GPUShaderModule: ...
    def create_compute_pipeline(
        self,
        layout: str,
        compute: ComputeDict,
    ) -> GPUComputePipeline: ...
    def create_bind_group(
        self,
        layout: GPUBindGroupLayout,
        entries: Sequence[BindGroupEntry],
    ) -> GPUBindGroup: ...

class GPUAdapter:
    def request_device_sync(
        self,
        *,
        label: str = "",
        required_features: Sequence[FeatureNameEnum] = (),
        required_limits: dict[str, int | None] | None = None,
        default_queue: QueueDescriptorStruct | None = None,
    ) -> GPUDevice: ...
