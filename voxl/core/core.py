import logging.config
from typing import final

from dependency_injector import containers, providers

from .asset_manager import AssetManager
from .camera import Camera
from .compute import ComputeManager
from .event_manager import EventManager


@final
class Core(containers.DeclarativeContainer):
    """The core functionality DI container.

    Attributes:
        config: The core configuration.
        logging: Logging configuration.
        asset_manager: The asset manager.
    """

    config = providers.Configuration()

    event_manager = providers.Singleton(EventManager)

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    asset_manager = providers.Singleton(
        AssetManager, config=config.asset_manager, event_manager=event_manager
    )

    camera = providers.Singleton(
        Camera,
        config=config.camera,
    )

    compute_manager = providers.ThreadLocalSingleton(
        ComputeManager, config=config.compute
    )
