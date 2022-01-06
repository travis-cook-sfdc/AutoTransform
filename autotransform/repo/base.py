#    _____          __       ___________                              _____                     
#   /  _  \  __ ___/  |_  ___\__    ___/___________    ____   _______/ ____\___________  _____  
#  /  /_\  \|  |  \   __\/  _ \|    |  \_  __ \__  \  /    \ /  ___/\   __\/  _ \_  __ \/     \ 
# /    |    \  |  /|  | (  <_> )    |   |  | \// __ \|   |  \\___ \  |  | (  <_> )  | \/  Y Y  \
# \____|__  /____/ |__|  \____/|____|   |__|  (____  /___|  /____  > |__|  \____/|__|  |__|_|  /
#         \/                                       \/     \/     \/                          \/ 

# Licensed under the MIT License <http://opensource.org/licenses/MIT
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Mapping, Optional, TypedDict

from autotransform.batcher.base import BatchWithFiles
from autotransform.repo.type import RepoType

class RepoBundle(TypedDict):
    params: Mapping[str, Any]
    type: RepoType

class Repo(ABC):
    params: Mapping[str, Any]
    
    def __init__(self, params: Mapping[str, Any]):
        self.params = params
        
    @abstractmethod
    def get_type(self) -> RepoType:
        pass
    
    @abstractmethod
    def has_changes(self, batch: BatchWithFiles) -> bool:
        pass
        
    @abstractmethod
    def submit(self, batch: BatchWithFiles) -> None:
        pass
    
    @abstractmethod
    def clean(self, batch: BatchWithFiles) -> None:
        pass
    
    @abstractmethod
    def rewind(self, batch: BatchWithFiles) -> None:
        pass
    
    def bundle(self) -> RepoBundle:
        return {
            "params": self.params,
            "type": self.get_type(),
        }
    
    @staticmethod
    @abstractmethod
    def from_data(data: Mapping[str, Any]) -> Repo:
        pass