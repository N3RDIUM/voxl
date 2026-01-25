from typing import final
from dependency_injector import containers, providers
import logging.config
from .asset_manager import AssetManager
from .camera import Camera


@final
class Core(containers.DeclarativeContainer):
    """The core functionality DI container.

    Attributes:
        config: The core configuration.
        logging: Logging configuration.
        asset_manager: The asset manager.
    """

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    asset_manager = providers.Resource(
        AssetManager,
        config=config.asset_manager,
    )

    camera = providers.Resource(
        Camera,
        config=config.camera,
    )
