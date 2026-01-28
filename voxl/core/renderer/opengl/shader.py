from pyglm import glm
from OpenGL.GL import (
    GL_FRAGMENT_SHADER,
    GL_VERTEX_SHADER,
    GL_FALSE,
    glGetUniformLocation,
    glUniform1f,
    glUniform1i,
    glUniform2f,
    glUniform3f,
    glUniform4f,
    glUniformMatrix2fv,
    glUniformMatrix3fv,
    glUniformMatrix4fv,
    glUniformMatrix2x3fv,
    glUniformMatrix3x2fv,
    glUniformMatrix2x4fv,
    glUniformMatrix4x2fv,
    glUniformMatrix3x4fv,
    glUniformMatrix4x3fv,
    glUseProgram,
)
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
            raise RuntimeError(f"Could not compile shader {self.name}: {e}")

        self.program = program

    def set_uniform(
        self,
        name: str,
        value: int
        | float
        | glm.vec2
        | glm.vec3
        | glm.vec4
        | glm.mat2
        | glm.mat3
        | glm.mat4
        | glm.mat2x3
        | glm.mat3x2
        | glm.mat2x4
        | glm.mat4x2
        | glm.mat3x4
        | glm.mat4x3,
    ) -> None:
        if self.program is None:
            raise RuntimeError(
                f"Tried to set shader {self.name} uniform(s) before compilation"
            )

        location = glGetUniformLocation(self.program, name)

        if isinstance(value, (int, bool)):
            glUniform1i(location, int(value))
        elif isinstance(value, float):
            glUniform1f(location, value)
        elif isinstance(value, glm.vec2):
            glUniform2f(location, value.x, value.y)
        elif isinstance(value, glm.vec3):
            glUniform3f(location, value.x, value.y, value.z)
        elif isinstance(value, glm.vec4):
            glUniform4f(location, value.x, value.y, value.z, value.w)
        elif isinstance(value, glm.mat2):
            glUniformMatrix2fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat3):
            glUniformMatrix3fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat2x3):
            glUniformMatrix2x3fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat3x2):
            glUniformMatrix3x2fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat2x4):
            glUniformMatrix2x4fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat4x2):
            glUniformMatrix4x2fv(location, 1, GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, glm.mat3x4):
            glUniformMatrix3x4fv(location, 1, GL_FALSE, glm.value_ptr(value))
        else:
            glUniformMatrix4x3fv(location, 1, GL_FALSE, glm.value_ptr(value))

    def use(self) -> None:
        if self.program is None:
            raise RuntimeError(
                f"Tried to use shader {self.name} before compilation"
            )

        glUseProgram(self.program)
