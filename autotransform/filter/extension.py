from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, TypedDict

from common.cachedfile import CachedFile
from filter.base import Filter
from filter.type import FilterType

class Extensions(str, Enum):
    PYTHON = ".py"
    TEXT = ".txt"
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

class ExtensionFilterParams(TypedDict):
    extensions: List[Extensions]

class ExtensionFilter(Filter):
    params: ExtensionFilterParams
    
    def __init__(self, params: ExtensionFilterParams):
        Filter.__init__(self, params)
    
    def get_type(self) -> FilterType:
        return FilterType.EXTENSION
        
    def _is_valid(self, file: CachedFile) -> bool:
        for extension in self.params["extensions"]:
            if file.path.endswith(extension):
                return True
        return False
    
    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ExtensionFilter:
        extensions = data["extensions"]
        assert isinstance(extensions, List)
        for extension in extensions:
            assert Extensions.has_value(extension)
        return cls({"extensions": extensions})