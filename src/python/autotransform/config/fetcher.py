# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

# @black_format

"""A base class for configuration fetching. Defines the API for fetching configuration
so that different components can be used that store configuration in different ways."""

from abc import abstractmethod
from enum import Enum

from autotransform.config.config import Config
from autotransform.util.component import Component, ComponentFactory, ComponentImport


class ConfigFetcherName(str, Enum):
    """A simple enum for mapping."""

    DEFAULT = "default"
    ENVIRONMENT = "environment"


class ConfigFetcher(Component):
    """An object representing the API needed for config fetching."""

    @abstractmethod
    def get_config(self) -> Config:
        """Fetch the Config.

        Returns:
            Config: The Config for AutoTransform.
        """


FACTORY = ComponentFactory(
    {
        ConfigFetcherName.DEFAULT: ComponentImport(
            class_name="DefaultConfigFetcher", module="autotransform.config.default"
        ),
        ConfigFetcherName.ENVIRONMENT: ComponentImport(
            class_name="EnvironmentConfigFetcher", module="autotransform.config.environment"
        ),
    },
    ConfigFetcher,  # type: ignore [misc]
    "config_fetcher.json",
)
