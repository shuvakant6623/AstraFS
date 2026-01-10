# 🚀 AstraFS
A Compiler-Driven Feature Store for Consistent ML Systems

AstraFS is a compiler-driven, strongly-typed, time-aware feature store designed to guarantee correctness, determinism, and offline–online consistency in machine learning systems.

Instead of treating features as database columns or ad-hoc Python functions, AstraFS treats features as first-class programs that are typed, versioned, and governed — and eventually compiled into deterministic execution plans.

This project is being built incrementally with a strong focus on ML systems, compiler-inspired design, and production-grade guarantees.
---
## 🚩 Motivation

In real-world ML systems, feature computation logic is often:

Duplicated across training and inference

Rewritten in different languages and pipelines

Difficult to audit, version, or reason about

This leads to:

Training–serving skew

Feature leakage

Silent model degradation

Non-reproducible experiments

AstraFS exists to solve this class of problems by treating feature computation as a typed, time-aware, compilable system rather than scattered code.
---
## 🧠 Core Idea

A feature store is not just a storage system —
it is a correctness system.

AstraFS enforces correctness by:

Making every feature time-aware

Giving every feature an explicit schema and owner

Ensuring the same definition is used for both training and serving

Preparing feature graphs for compiler-style analysis and optimization
---
## 🔑 System Invariants (Non-Negotiable)

Every layer of AstraFS is designed around these invariants:

Time Awareness
All features must be computed at an explicit event time to prevent future data leakage.

Single Source of Truth
A feature is defined once and reused everywhere — no duplicate logic.

Offline–Online Consistency
Training and serving must be derived from the same feature definition.

Determinism
Given the same data and time context, feature computation must be reproducible.

Explicit Dependencies
Feature dependencies must be declared and tracked — never implicit.

These invariants are enforced starting from the lowest level of the system.
---
## 🧩 What Is Implemented So Far (Foundation Phase)

The first phase builds the type system and registry of the feature store.

This is the foundation that all future compiler, planner, and execution layers will rely on.

Implemented Components
core/feature.py

Defines the Feature Language:

FeatureMetadata

Immutable schema of a feature

Name, entity, value type, description, owner

Acts like the type definition of a feature

Feature

Abstract base class for all features

Enforces:

Time-aware computation

Type-safe output

A single execution path for validation

A feature in AstraFS is:

A deterministic, typed function of raw data at a specific time.

core/metadata.py

Defines the Feature Registry & Versioning System:

FeatureKey
Uniquely identifies a feature as (name, entity)

FeatureSpec
Represents one version of a feature, including:

Metadata

Version

Creation time

Dependencies

Active / deprecated state

FeatureRegistry
A global catalog that:

Registers features

Tracks versions

Resolves the latest active definition

Records feature dependencies

This allows AstraFS to support:

Safe feature evolution

Reproducible training

Dependency-aware compilation in later phases
---
## 📁 Current Project Structure
```bash
astrafs/
├── core/
│   ├── feature.py      # Feature type system
│   └── metadata.py     # Feature registry & versioning
│
├── docs/               # Design notes and invariants (in progress)
├── examples/           # Feature definitions (in progress)
└── tests/              # Unit tests (in progress)
```

Only the foundation layer is implemented at this stage.

## 🛣️ Roadmap

Phase 1 — Feature Language & Registry

Feature type system

Feature metadata & immutability

Feature registry & versioning

Dependency tracking

Phase 2 — Feature Compiler

Feature AST

Semantic analysis (type & time checking)

Dependency graph construction

Phase 3 — Planner & Execution

Deterministic DAG planner

Offline & online execution engines

Guaranteed offline–online parity
---
## 🎯 Long-Term Vision

AstraFS aims to become:

A compiler-aware feature store

A system with strong correctness guarantees

A platform for exploring ML systems, compilers, and data infrastructure

This is a systems engineering project, not a demo or notebook.
---
## 📖 Documentation

Design notes, invariants, and architectural reasoning live in the docs/ directory.