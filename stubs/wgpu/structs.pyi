from typing import Mapping, TypedDict

from wgpu.classes import GPUBuffer

type QueueDescriptorStruct = Mapping[str, str] | dict[str, str]

class BindGroupEntry(TypedDict):
    binding: int
    resource: GPUBuffer
