from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class FeatureMetadata:
    name: str
    entity: str
    value_type: type
    description: str
    owner: str

class Feature(ABC):
    def __init__(self, metadata: FeatureMetadata):
        self._metadata = metadata

    
    @property
    def name(self) -> str:
        return self._metadata.name
    
    @property 
    def entity(self) -> str:
        return self._metadata.entity

    @property
    def value_type(self) -> type:
        return self._metadata.value_type
    
    @abstractmethod
    def compute(
        self,
        raw_data: Dict[str, Any],
        event_time: datetime
    ) -> Any:
        pass

    def validate(self, value: Any) -> None:
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"Feature '{self.name}' expected value of type"
                f"{self.value_type.__name__}, got {type(value).__name__}"
            )


    def evaluate (
        self, 
        raw_data: Dict[str, Any],
        event_time: datetime
    ) -> Any:
        value = self.compute(raw_data, event_time)
        self.validate(value)

    
    def sinature(self) -> Dict[str, Any]:

        return {
            "name" : self.name,
            "entity" : self.entity,
            "value_type" : self.value_type.__name__,
        }