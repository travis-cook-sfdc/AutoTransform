from __future__ import annotations
from typing import Any, Dict, List, TypedDict

from batcher.base import Batch, Batcher
from batcher.type import BatcherType
from common.cachedfile import CachedFile

class SingleBatcherParams(TypedDict):
    message: str

class SingleBatcher(Batcher):
    params: SingleBatcherParams
    
    def __init__(self, params: SingleBatcherParams):
        Batcher.__init__(self, params)
        
    def get_type(self) -> BatcherType:
        return BatcherType.SINGLE
        
    def batch(self, files: List[CachedFile]) -> List[Batch]:
        batch: Batch = {
            "files": list(range(len(files))),
            "metadata": {"message": self.params["message"]},
        }
        return [batch]
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> SingleBatcher:
        message = data["message"]
        assert isinstance(message, str)
        return cls({"message": message})