"""Asset manager which handles loading textures and shaders.

This util only loads the images and shader code into memory, and makes them
accessible using a unique id. The actual image stuff or shader compilation is
handled by the individual render backends themselves.

Todo:
    * Implement compute shader loading capabilities
    * Implement image asset loading capabilities
"""

import logging
import os
from time import perf_counter
from typing import TypedDict

from PIL import Image
import numpy as np
from voxl.core.events import AssetsLoaded
from voxl.constants import TEXTURE_SUFFIX_WHITELIST

from .event_manager import EventManager


class AssetManagerConfig(TypedDict):
    """Asset manager config TypedDict."""

    ...


default_config: AssetManagerConfig = {}


class AssetManager:
    shaders: dict[str, dict[str, str]]
    textures: dict[str, np.ndarray]
    config: AssetManagerConfig
    logger: logging.Logger
    event_manager: EventManager

    def __init__(
        self, config: AssetManagerConfig | None, event_manager: EventManager
    ) -> None:
        self.shaders = {}
        self.textures = {}
        self.event_manager = event_manager

        if config is None:
            config = default_config
        self.config = config

        self.logger = logging.getLogger("AssetManager")

    def load_assets(self, asset_dir: str, prefix: str) -> None:
        """Load assets from a given dir, assign IDs with the given prefix.

        Currently loads all vertex and fragment shaders. Corresponding .vert and
        .frag files must have the same name (without the extension, of course).
        For example, foo.frag and foo.vert
        """

        self.logger.info(f"Loading assets from {asset_dir} as {prefix}")

        t0 = perf_counter()

        shader_dir = os.path.join(asset_dir, "shaders/")
        texture_dir = os.path.join(asset_dir, "textures/")

        self.logger.info("\tLoading shaders")
        shader_pairs: set[str] = set()
        for file in os.listdir(shader_dir):
            name = file.split(".")[0]
            shader_pairs.add(name)

        for name in shader_pairs:
            self.logger.info(f"\t- {prefix}:{name}")

            vert_path = os.path.join(shader_dir, name + ".vert")
            frag_path = os.path.join(shader_dir, name + ".frag")

            try:
                with open(vert_path) as f:
                    vert: str = f.read()
            except FileNotFoundError:
                raise Exception(
                    f"Shader not found: {vert_path} required for {frag_path}"
                )

            try:
                with open(frag_path) as f:
                    frag: str = f.read()
            except FileNotFoundError:
                raise Exception(
                    f"Shader not found: {frag_path} required for {vert_path}"
                )

            self.shaders[f"{prefix}:{name}"] = {"vert": vert, "frag": frag}

        self.logger.info("\tLoading assets")
        for file in os.listdir(texture_dir):
            if "." not in file or file.startswith(".") or file.endswith("."):
                continue

            if file.split(".")[-1] not in TEXTURE_SUFFIX_WHITELIST:
                continue

            name = ".".join(file.split(".")[:-1])
            self.logger.info(f"\t- {prefix}:{name}")

            fullpath = os.path.join(texture_dir, file)
            texture = Image.open(fullpath)
            self.textures[f"{prefix}:{name}"] = np.array(texture.getdata())

        self.logger.info(
            f"\tAsset load {prefix} took {perf_counter() - t0} sec"
        )
        self.event_manager.emit(AssetsLoaded(prefix=prefix))

    def get_shader(self, name: str) -> dict[str, str]:
        # TODO TypedDict ShaderCode
        if name not in self.shaders:
            raise Exception(
                f"Tried to get shader {name},"
                + " but it doesn't exist or isn't loaded yet"
            )
        return self.shaders[name]
