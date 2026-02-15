"""
AKN Profiler — Pydantic Models

This subpackage contains Pydantic BaseModel classes representing:

  - AKN schema elements and their attributes/constraints
  - Application profile restriction rules (what is allowed, required,
    forbidden, or narrowed from the full AKN schema)
  - The profile document structure itself (the YAML schema)

The models are derived from the parsed XSD and serve as the single
source of truth for validation, completion suggestions, and
auto-generation of minimum viable profiles.
"""
