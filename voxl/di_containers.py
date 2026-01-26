"""Dependency Injection Containers.

Todo:
    * Error handling for the backend selectors
"""

from typing import final
from dependency_injector import containers, providers

from .core import windowing
from .core import renderer
from .core import Core


@final
class Voxl(containers.DeclarativeContainer):
    """The main application DI container for Voxl.

    Attributes:
        config: The configuration to use
        core: The `Core` DI container: :py:class:`voxl.core.core.Core`
        window: The window, backend configured using the configuration file.
        renderer: The renderer, backend configured using the configuration file.
    """

    config = providers.Configuration()

    core = providers.Container(Core, config=config.core)

    window = providers.Selector(
        config.window.backend,  # todo error handling for unexpected backend str
        headless=providers.Singleton(windowing.Window, config=config.window),
        glfw=providers.ThreadLocalSingleton(  # glfw isnt thread-safe
            windowing.GlfwWindow, config=config.window, core=core
        ),
    )

    renderer = providers.Selector(
        config.renderer.backend,
        none=providers.Singleton(
            renderer.Renderer, config=config.renderer, window=window, core=core
        ),
        opengl=providers.ThreadLocalSingleton(  # opengl isnt thread-safe
            renderer.OpenGLRenderer,
            config=config.renderer,
            window=window,
            core=core,
        ),
    )
