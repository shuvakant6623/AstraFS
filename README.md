# AstraFS

## A Compiler-Driven Feature Store for Consistent ML Systems

AstraFS is a feature store designed to **guarantee correctness, consistency, and reuse of machine learning features** across training and serving by compiling feature definitions into a single, optimized execution plan.

This project is being built incrementally with a strong focus on **ML systems, compiler-inspired design, and production guarantees** rather than quick experimentation.

---

## 🚩 Motivation

In real-world ML systems, feature computation logic is often:
- Duplicated across training and inference
- Rewritten in different languages and pipelines
- Difficult to audit, version, or optimize

This leads to **training–serving skew**, **feature leakage**, and **silent model degradation**.

AstraFS exists to solve this class of problems by treating feature computation as a **first-class, compilable system**, not ad-hoc code.

---

## 🧠 Core Idea

> A feature store is not just storage for features —  
> it is a system that enforces **correctness guarantees**.

AstraFS enforces these guarantees by:
- Making feature definitions **explicit and time-aware**
- Ensuring the **same logic** powers both offline and online computation
- Representing feature computation as a **dependency graph**
- Preparing for compiler-style optimization and lowering

---

## 🔑 System Invariants (Non-Negotiable)

The following invariants guide every design decision in AstraFS:

1. **Time Awareness**  
   Every feature must be explicitly time-indexed to prevent feature leakage.

2. **Single Source of Truth**  
   A feature is defined once and reused for both training and serving.

3. **Offline–Online Consistency**  
   Offline and online feature computation must be derived from the same execution plan.

4. **Determinism**  
   Given the same inputs and time context, feature computation must be deterministic.

5. **Explicit Dependencies**  
   Feature dependencies must be declared and resolved explicitly—never implicitly.

These invariants are defined early to avoid accidental complexity later.

---

## 🏗️ Project Structure (Initial)

```text
astra_fs/
├── frontend/     # Feature definitions and DSL (future)
├── ir/           # Intermediate representation of feature graphs
├── optimizer/    # Compiler-style optimization passes
├── backends/     # Offline and online execution backends
├── serving/      # Online serving engine
├── docs/         # Design notes and invariants
└── README.md
```

This structure will evolve as the system matures.

---

## 🛣️ Current Status

**Foundation Phase (In Progress)**

- Problem space defined
- Core system invariants established
- Project structure initialized

Early development is focused on correctness and design clarity.

---

## 🎯 Long-Term Goals

**AstraFS aims to grow into:**

- A compiler-aware feature store with optimization passes

- A system with strong offline–online consistency guarantees

- A learning vehicle for ML systems, compilers, and distributed data infrastructure

This is a long-term, systems-focused project, not a demo.

---

## 📌 Notes

- Early versions will prioritize correctness over performance

- Compiler concepts will be introduced gradually and only when justified

- The project is intentionally built in public to document real design trade-offs

## 📖 Documentation

- Design notes, invariants, and architectural decisions live in the docs/ directory.