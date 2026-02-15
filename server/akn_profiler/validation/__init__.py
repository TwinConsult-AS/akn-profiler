"""
AKN Profiler — Profile Validation

This subpackage validates user-written YAML application profiles
against the Pydantic models derived from the AKN XSD schema.

Responsibilities:
  - Parse and deserialise .akn.yaml files
  - Validate profile restrictions against the full AKN schema
    (e.g. ensuring a restricted element actually exists, an attribute
    enum subset is valid, cardinality constraints are tighter than
    the original, etc.)
  - Produce LSP Diagnostic objects for any validation errors/warnings
  - Support incremental re-validation on document edits
"""
