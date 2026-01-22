"""Voxl entry point

Initializes everything, loads the configuration from `config.yml` in the cwd,
handles program startup and post-termination cleanups.
"""

from dependency_injector.wiring import Provide, inject

from voxl.core.compute import ComputeManager
from voxl.core.windowing.headless import Window
from voxl.core.renderer.renderer import Renderer
from voxl.di_containers import Voxl


@inject
def main(
    compute_manager: ComputeManager = Provide[Voxl.compute_manager],
    renderer: Renderer = Provide[Voxl.renderer],
    window: Window = Provide[Voxl.window],
) -> None:
    """The main entry point.

    Starts the application mainloop and handles after-close cleanup.
    """
    _ = renderer, compute_manager

    try:
        window.mainloop()
    except KeyboardInterrupt:
        ...

    # TODO cleanup


if __name__ == "__main__":
    app = Voxl()

    app.config.from_yaml("config.yml")

    core = app.core()
    core.logging()

    app.wire(modules=[__name__])
    main()
