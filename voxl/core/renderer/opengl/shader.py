from OpenGL.GL import GL_FRAGMENT_SHADER, GL_VERTEX_SHADER, glUseProgram
from OpenGL.GL.shaders import (
    compileProgram,
    compileShader,
    ShaderProgram,
    ShaderCompilationError,
)
from voxl.core.asset_manager import AssetManager
from logging import getLogger, Logger


class OpenGLShader:
    """Simple wrapper for handling OpenGL shaders

    Interfaces with the AssetManager to handle shader code compilation, as well
    as usage.
    """

    name: str
    asset_manager: AssetManager
    program: ShaderProgram | None
    logger: Logger

    def __init__(self, name: str, asset_manager: AssetManager) -> None:
        self.name = name
        self.asset_manager = asset_manager
        self.program = None
        self.logger = getLogger("OpenGLShader")

    def compile(self) -> None:
        shader_src = self.asset_manager.get_shader(self.name)
        vert_src, frag_src = shader_src["vert"], shader_src["frag"]

        self.logger.info(f"Compiling shader {self.name}")
        try:
            vert = compileShader(vert_src, GL_VERTEX_SHADER)
            frag = compileShader(frag_src, GL_FRAGMENT_SHADER)
            program = compileProgram(vert, frag)
        except ShaderCompilationError as e:
            raise Exception(f"Could not compile shader {self.name}: {e}")

        self.program = program

    def use(self) -> None:
        if self.program is None:
            raise Exception(
                f"Tried to use shader {self.name} before compilation"
            )

        glUseProgram(self.program)
