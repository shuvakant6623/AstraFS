from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


# ================================
# FeatureMetadata
# ================================
# This object describes a feature at the *schema and governance level*.
# It does NOT contain data — only the contract that defines what the feature means.
#
# Why this exists:
# In real ML systems, a feature is not "just a number".
# It must have:
# - a stable name
# - an entity it belongs to
# - a data type
# - ownership (who is responsible for it)
#
# This prevents:
# - silent breaking changes
# - duplicate features
# - training/serving mismatches
#
# frozen=True ensures this metadata is immutable after creation.
# That guarantees that once a feature is defined, its contract cannot be mutated.
@dataclass(frozen=True)
class FeatureMetadata:
    name: str            # Unique feature name (e.g. "user_7d_spend")
    entity: str          # Entity this feature belongs to (e.g. "user", "merchant")
    value_type: type     # Python type of the feature (int, float, bool, etc)
    description: str     # Human-readable meaning of the feature
    owner: str           # Team or person responsible for this feature


# ================================
# Feature (Abstract Base Class)
# ================================
# This is the core abstraction of the feature store.
#
# A Feature represents:
#   "A deterministic function of raw data at a given point in time"
#
# This abstraction is what allows:
# - Offline and online pipelines to share the same logic
# - Point-in-time correctness
# - Compiler optimization of feature graphs
#
# Concrete features will subclass this and implement compute()
class Feature(ABC):

    def __init__(self, metadata: FeatureMetadata):
        # We store metadata instead of separate fields
        # so that schema, ownership and typing move together
        self._metadata = metadata

    # Expose metadata fields as read-only properties.
    # This prevents accidental mutation of feature definitions.
    @property
    def name(self) -> str:
        return self._metadata.name
    
    @property 
    def entity(self) -> str:
        return self._metadata.entity

    @property
    def value_type(self) -> type:
        return self._metadata.value_type
    

    # ----------------------------------
    # compute()
    # ----------------------------------
    # This is the ONLY method feature authors must implement.
    #
    # It defines how the feature is derived from:
    # - raw_data (logs, tables, events)
    # - event_time (the point in time we are computing for)
    #
    # event_time is critical:
    # It prevents future data leakage by enforcing time-aware computation.
    @abstractmethod
    def compute(
        self,
        raw_data: Dict[str, Any],
        event_time: datetime
    ) -> Any:
        pass


    # ----------------------------------
    # validate()
    # ----------------------------------
    # This enforces the feature contract at runtime.
    #
    # Why this matters:
    # If training produces float but serving produces int,
    # the model will silently degrade.
    #
    # This catches those bugs early.
    def validate(self, value: Any) -> None:
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"Feature '{self.name}' expected value of type "
                f"{self.value_type.__name__}, got {type(value).__name__}"
            )


    # ----------------------------------
    # evaluate()
    # ----------------------------------
    # This is the execution wrapper around compute().
    #
    # All feature computation should go through this path so that:
    # - type validation always happens
    # - future hooks (logging, caching, lineage) can be added here
    def evaluate (
        self, 
        raw_data: Dict[str, Any],
        event_time: datetime
    ) -> Any:
        value = self.compute(raw_data, event_time)
        self.validate(value)
        return value


    # ----------------------------------
    # signature()
    # ----------------------------------
    # This returns a stable, serializable description of the feature.
    #
    # This is what the compiler, registry, and dependency graph will use.
    # It allows features to be:
    # - hashed
    # - compared
    # - versioned
    def signature(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "entity": self.entity,
            "value_type": self.value_type.__name__,
        }
