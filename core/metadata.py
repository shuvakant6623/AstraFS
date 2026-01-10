from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Set
from uuid import uuid4

from feature import FeatureMetadata


# -----------------------------------
# FeatureKey
# -----------------------------------
# A globally unique identity for a feature.
# (name, entity) together define what the feature is.
@dataclass(frozen=True)
class FeatureKey:
    name: str
    entity: str


# -----------------------------------
# FeatureSpec
# -----------------------------------
# One specific version of a feature.
# This is what the compiler and registry operate on.
@dataclass
class FeatureSpec:
    key: FeatureKey
    metadata: FeatureMetadata
    version: str
    created_at: datetime
    dependencies: Set[FeatureKey]
    is_active: bool = True
    is_deprecated: bool = False


# -----------------------------------
# FeatureRegistry
# -----------------------------------
class FeatureRegistry:

    def __init__(self):
        # Stores all feature versions
        # Keyed by (FeatureKey, version)
        self._store: Dict[Tuple[FeatureKey, str], FeatureSpec] = {}

        # Tracks latest active version for each feature
        self._latest: Dict[FeatureKey, str] = {}


    # ----------------------------
    # Register a new feature
    # ----------------------------
    def register(
        self,
        metadata: FeatureMetadata,
        dependencies: Set[FeatureKey]
    ) -> FeatureSpec:
        
        key = FeatureKey(metadata.name, metadata.entity)

        # Generate a new version id
        version = str(uuid4())[:8]

        spec = FeatureSpec(
            key=key,
            metadata=metadata,
            version=version,
            created_at=datetime.utcnow(),
            dependencies=dependencies
        )

        # Enforce uniqueness of version
        self._store[(key, version)] = spec

        # Mark this as the latest active version
        self._latest[key] = version

        return spec


    # ----------------------------
    # Get latest active feature
    # ----------------------------
    def get(self, name: str, entity: str) -> FeatureSpec:
        key = FeatureKey(name, entity)

        if key not in self._latest:
            raise KeyError(f"Feature {name}:{entity} not found")

        version = self._latest[key]
        return self._store[(key, version)]


    # ----------------------------
    # Deprecate a feature
    # ----------------------------
    def deprecate(self, name: str, entity: str):
        key = FeatureKey(name, entity)

        if key not in self._latest:
            raise KeyError(f"Feature {name}:{entity} not found")

        version = self._latest[key]
        spec = self._store[(key, version)]

        spec.is_active = False
        spec.is_deprecated = True

        del self._latest[key]


    # ----------------------------
    # Dependency graph for compiler
    # ----------------------------
    def dependency_graph(self) -> Dict[FeatureKey, Set[FeatureKey]]:
        graph: Dict[FeatureKey, Set[FeatureKey]] = {}

        for (key, _), spec in self._store.items():
            graph[key] = spec.dependencies
            
        return graph
