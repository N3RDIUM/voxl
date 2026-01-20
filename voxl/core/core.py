from typing import final
from dependency_injector import containers, providers
import logging.config

@final
class Core(containers.DeclarativeContainer):
    """The core functionality DI container. Implements logging.

    Attributes:
        config: The core configuration.

    """

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
