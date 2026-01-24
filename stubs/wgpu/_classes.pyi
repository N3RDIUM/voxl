from wgpu._coreutils import CanvasLike
from wgpu.classes import GPUAdapter
from wgpu.enums import PowerPreferenceEnum

class GPU:
    def request_adapter_sync(
        self,
        *,
        feature_level: str = "core",
        power_preference: PowerPreferenceEnum
        | str
        | None = None,  # TODO verify
        force_fallback_adapter: bool = False,
        canvas: CanvasLike | None = None,
    ) -> GPUAdapter: ...
