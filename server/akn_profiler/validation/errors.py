"""
Validation error types for the AKN Profiler.

Every rule module produces ``ValidationError`` instances.  The engine
collects them and (later) the server converts them to LSP Diagnostics.
"""

from __future__ import annotations

import dataclasses
from enum import Enum


class Severity(Enum):
    """Maps to LSP DiagnosticSeverity values."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclasses.dataclass(frozen=True)
class ValidationError:
    """A single validation finding against a profile YAML document.

    Attributes
    ----------
    rule_id:
        Dot-separated identifier.  The prefix is the rule category:
        ``vocabulary``, ``structure``, ``datatype``, ``identity``.
        Examples: ``vocabulary.unknown-element``,
        ``datatype.invalid-enum-value``.
    path:
        YAML key path where the error was detected.
        Example: ``profile.elements.act.children[2]``
    message:
        Human-readable description of the problem.
    severity:
        Error / warning / informational.
    line:
        1-based line number in the YAML source (``None`` when unknown).
    column:
        0-based column offset (``None`` when unknown).
    """

    rule_id: str
    path: str
    message: str
    severity: Severity = Severity.ERROR
    line: int | None = None
    column: int | None = None
