"""Simple camera/MVP helper."""

from typing import TypedDict
from pyglm import glm
from voxl.default_config import DEFAULT_FOV, DEFAULT_NEAR, DEFAULT_FAR


class CameraConfig(TypedDict):
    """Camera configuration.

    Attributes:
        fov: The field of view of the camera in degrees.
        near: The distance to the near clipping plane.
        far: The distance to the far clipping plane.
    """

    fov: float
    near: float
    far: float


default_config: CameraConfig = {
    "fov": DEFAULT_FOV,
    "near": DEFAULT_NEAR,
    "far": DEFAULT_FAR,
}


class Camera:
    """Simple movable/rotatable camera.

    Implements configurable FOV, near/far clipping planes.
    """

    config: CameraConfig
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]

    def __init__(self, config: CameraConfig | None) -> None:
        if config is None:
            config = default_config
        self.config = config

        self.position = (0.0, 0.0, 0.0)
        self.rotation = (0.0, 0.0, 0.0)

    def generate_mvp(
        self, viewport_size: tuple[int, int]
    ) -> tuple[glm.mat4, glm.mat4]:
        """Generate the model view projection matrices."""

        matrix = glm.mat4(1.0)

        for i in range(3):
            axis = glm.vec3(0.0)
            axis[i] = 1.0

            matrix = glm.rotate(matrix, glm.radians(self.rotation[i]), axis)

        matrix = glm.translate(matrix, glm.vec3(self.position))

        width, height = viewport_size
        aspect = 1
        if height != 0:
            aspect = width / height

        projection = glm.perspective(
            self.config.get("fov", DEFAULT_FOV),
            aspect,
            self.config.get("far", DEFAULT_FAR),
            self.config.get("near", DEFAULT_NEAR),
        )

        return matrix, projection
