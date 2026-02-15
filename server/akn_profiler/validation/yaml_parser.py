"""
YAML parser with source-location tracking.

Parses ``.akn.yaml`` text into a ``ProfileDocument`` **and** records
the 1-based line number of every mapping key so that validation errors
can point at the exact YAML line.

Public API
----------
``parse_profile(yaml_text) -> (ProfileDocument | None, list[ValidationError], LineIndex)``
"""

from __future__ import annotations

import logging

import yaml
from pydantic import ValidationError as PydanticValidationError

from akn_profiler.models.profile import ProfileDocument
from akn_profiler.validation.errors import Severity, ValidationError

logger = logging.getLogger(__name__)


class LineIndex:
    """Maps YAML key paths to their 1-based source line numbers.

    Built during YAML loading by using ``yaml.compose()`` which returns
    a node tree that retains ``start_mark`` positions.
    """

    def __init__(self) -> None:
        self._lines: dict[str, int] = {}

    def set(self, path: str, line: int) -> None:
        self._lines[path] = line

    def get(self, path: str) -> int | None:
        """Return the 1-based line for *path*, or ``None``."""
        return self._lines.get(path)

    def get_or(self, path: str, fallback: int = 1) -> int:
        return self._lines.get(path, fallback)


def _walk_node(node: yaml.Node, prefix: str, index: LineIndex) -> None:
    """Recursively walk a YAML node tree and record key positions."""
    if isinstance(node, yaml.MappingNode):
        for key_node, value_node in node.value:
            if isinstance(key_node, yaml.ScalarNode):
                key_str = key_node.value
                path = f"{prefix}.{key_str}" if prefix else key_str
                # +1 because yaml marks are 0-based
                index.set(path, key_node.start_mark.line + 1)
                _walk_node(value_node, path, index)
    elif isinstance(node, yaml.SequenceNode):
        for i, item_node in enumerate(node.value):
            path = f"{prefix}[{i}]"
            index.set(path, item_node.start_mark.line + 1)
            _walk_node(item_node, path, index)


def _build_line_index(yaml_text: str) -> LineIndex:
    """Compose the YAML and record line numbers for every key."""
    index = LineIndex()
    try:
        root = yaml.compose(yaml_text, Loader=yaml.SafeLoader)
        if root is not None:
            _walk_node(root, "", index)
    except yaml.YAMLError:
        pass  # syntax errors are reported separately
    return index


def parse_profile(
    yaml_text: str,
) -> tuple[ProfileDocument | None, list[ValidationError], LineIndex]:
    """Parse raw YAML text into a validated ``ProfileDocument``.

    Returns
    -------
    (profile, errors, line_index)
        ``profile`` is ``None`` when parsing or structural validation
        fails.  ``errors`` contains any YAML syntax or Pydantic
        validation errors.  ``line_index`` maps YAML paths → line
        numbers regardless of whether parsing succeeded.
    """
    line_index = _build_line_index(yaml_text)
    errors: list[ValidationError] = []

    # --- Step 1: YAML syntax ----------------------------------------
    try:
        raw = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        line: int | None = None
        if hasattr(exc, "problem_mark") and exc.problem_mark is not None:
            line = exc.problem_mark.line + 1
        errors.append(
            ValidationError(
                rule_id="parse.yaml-syntax",
                path="",
                message=f"YAML syntax error: {exc}",
                severity=Severity.ERROR,
                line=line,
            )
        )
        return None, errors, line_index

    if not isinstance(raw, dict):
        errors.append(
            ValidationError(
                rule_id="parse.not-a-mapping",
                path="",
                message=(
                    "Profile must be a YAML mapping. Start with 'profile:' at the top of the file."
                ),
                severity=Severity.ERROR,
                line=1,
            )
        )
        return None, errors, line_index

    # --- Step 2: Extract the 'profile' top-level key ----------------
    profile_data = raw.get("profile")
    if profile_data is None:
        errors.append(
            ValidationError(
                rule_id="parse.missing-profile-key",
                path="",
                message="Missing top-level 'profile' key",
                severity=Severity.ERROR,
                line=1,
            )
        )
        return None, errors, line_index

    if not isinstance(profile_data, dict):
        errors.append(
            ValidationError(
                rule_id="parse.profile-not-mapping",
                path="profile",
                message="'profile' must be a mapping",
                severity=Severity.ERROR,
                line=line_index.get("profile"),
            )
        )
        return None, errors, line_index

    # --- Step 3: Pydantic structural validation ----------------------
    try:
        profile = ProfileDocument.model_validate(profile_data)
    except PydanticValidationError as exc:
        for err in exc.errors():
            loc_parts = [str(p) for p in err.get("loc", ())]
            path = "profile." + ".".join(loc_parts) if loc_parts else "profile"
            errors.append(
                ValidationError(
                    rule_id="parse.pydantic",
                    path=path,
                    message=err.get("msg", str(err)),
                    severity=Severity.ERROR,
                    line=line_index.get(path),
                )
            )
        return None, errors, line_index

    return profile, errors, line_index
