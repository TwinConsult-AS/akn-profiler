"""
Validation engine — orchestrates all rule modules.

Public API::

    from akn_profiler.validation.engine import validate_profile

    errors = validate_profile(yaml_text, schema)
    for e in errors:
        print(f"[{e.rule_id}] line {e.line}: {e.message}")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from akn_profiler.validation import (
    rules_choice,
    rules_datatype,
    rules_identity,
    rules_strictness,
    rules_structure,
    rules_vocabulary,
)
from akn_profiler.validation.errors import ValidationError
from akn_profiler.validation.yaml_parser import parse_profile

if TYPE_CHECKING:
    from akn_profiler.xsd.schema_loader import AknSchema

logger = logging.getLogger(__name__)

# Ordered list of rule modules.  Each must expose:
#   validate(profile, schema, line_index) -> list[ValidationError]
_RULE_MODULES = [
    rules_vocabulary,
    rules_structure,
    rules_choice,
    rules_datatype,
    rules_identity,
    rules_strictness,
]


def validate_profile(
    yaml_text: str,
    schema: AknSchema,
) -> list[ValidationError]:
    """Run the full validation pipeline on a YAML profile string.

    1. Parse YAML into a ``ProfileDocument`` (structural validation).
    2. Run each rule module in order (XSD cross-validation).
    3. Return the combined, deduplicated error list.
    """
    profile, parse_errors, line_index = parse_profile(yaml_text)

    if profile is None:
        # Structural problems — can't run XSD rules
        return parse_errors

    all_errors: list[ValidationError] = list(parse_errors)

    for module in _RULE_MODULES:
        try:
            module_errors = module.validate(profile, schema, line_index)
            all_errors.extend(module_errors)
        except Exception:
            logger.exception("Rule module %s raised an exception", module.__name__)

    return _deduplicate(all_errors)


def _deduplicate(errors: list[ValidationError]) -> list[ValidationError]:
    """Remove identical errors (same rule_id + path + message)."""
    seen: set[tuple[str, str, str]] = set()
    result: list[ValidationError] = []
    for e in errors:
        key = (e.rule_id, e.path, e.message)
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result
