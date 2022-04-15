# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

"""A base class for configuration fetching."""

from abc import ABC, abstractmethod
from typing import List, Optional


class ConfigFetcher(ABC):
    """An object representing the API needed for config fetching."""

    @abstractmethod
    def get_github_token(self) -> Optional[str]:
        """Fetch the github token from configuration

        Returns:
            Optional[str]: The github token
        """

    @abstractmethod
    def get_github_username(self) -> Optional[str]:
        """Fetch the github username from configuration

        Returns:
            Optional[str]: The github username
        """

    @abstractmethod
    def get_github_password(self) -> Optional[str]:
        """Fetch the github password from configuration

        Returns:
            Optional[str]: The github password
        """

    @abstractmethod
    def get_github_base_url(self) -> Optional[str]:
        """Fetch the github base URL from configuration

        Returns:
            Optional[str]: The github base URL
        """

    @abstractmethod
    def get_component_imports(self) -> List[str]:
        """The modules containing the custom components to use: see autotransform.thirdparty.example

        Returns:
            List[str]: A list of the modules containing custom components that are not part base
                AutoTransform
        """

    @abstractmethod
    def get_remote(self) -> Optional[str]:
        """Gets the JSON encoded Remote component to use

        Returns:
            str: The JSON encoded Remote component to use
        """
