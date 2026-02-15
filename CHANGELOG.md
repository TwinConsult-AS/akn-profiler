# Changelog

All notable changes to the AKN Profiler extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-02-15

### Added

- **XSD Choice Group support** — new `choice:` key inside `children:` for declaring mutually exclusive child branches using a flat dict format.
- **Choice parser** — `choice_parser.py` dynamically extracts `xs:choice` and `xs:group` structures from the AKN 3.0 XSD, resolving nested group references and branch membership.
- **Choice validation rules** — five new diagnostics powered by the `rules_choice` module:
  - `choice.required-group-empty` — mandatory choice group has no members declared.
  - `choice.incomplete-branches` — `choice:` has fewer than 2 alternatives.
  - `choice.exclusive-branch-conflict` — children from multiple exclusive branches mixed in `children:`.
  - `choice.branch-invalid-child` — `choice:` branch contains an element not valid per the XSD.
  - `choice.branch-overlap` — element appears in both `children:` and `choice:`.
- **Cross-block exclusion** — elements listed in `children:` are excluded from `choice:` completions and vice-versa, preventing duplicate declarations.
- **Choice hover documentation** — "Either/or" summary for exclusive choice groups on element hover; dedicated hover for the `choice:` key with example YAML.
- **Auto-suggest chaining** — after inserting `choice:`, the extension automatically prompts for the first two branch elements with correct indentation.
- **Choice code actions** — quick-fix suggestions for exclusive-branch conflicts (remove conflicting child, use `choice:`).
- **Cascading lightbulb actions** — "Add child" and "Add attribute" lightbulbs are now visible from any nested scope (children, choice, attributes), not just the immediate block.
- **Undeclared choice child detection** — `strictness.undeclared-child-element` now also checks elements inside `choice:` branches.

### Changed

- Generator output now includes `choice:` blocks for elements with exclusive XSD choice groups (e.g. hierarchy types).
- Cascade expand/collapse correctly handles `choice:` — expand builds exclusive branches, collapse preserves the `choice:` key.
- `_find_element_context` improved — recognises bare element entries and handles `choice` as a structural key.

### Infrastructure

- Test suite expanded to 250 tests covering all new choice functionality.
- New test modules: `test_rules_choice.py` (choice validation rules), plus extended coverage in `test_cascade.py`, `test_code_actions_add.py`, `test_engine.py`, `test_generator.py`, `test_rules_strictness.py`, `test_schema_loader.py`, `test_yaml_context.py`.

## [0.1.0] — 2026-02-15

### Added

- **Language support** for `.akn.yaml` / `.akn.yml` files with TextMate grammar and semantic highlighting.
- **Auto-completion** — context-aware suggestions for profile keys, AKN element names, attribute names, document types, enum values, children, and structure entries.
- **Inline diagnostics** — real-time validation engine with rule modules for vocabulary, structure, data types, identity, and strictness.
- **Hover documentation** — XSD-sourced documentation for AKN elements, attributes, profile keys, and cardinality.
- **Code actions** — diagnostic-based quick-fixes (typo correction, scaffold insertion) and contextual "Add …" lightbulb actions for children, attributes, and values.
- **Code lens** — "Initialize Profile Scaffold" button on empty `.akn.yaml` files.
- **Semantic tokens** — full semantic highlighting for element names, attributes, keywords, enum values, child references, cardinality, and booleans.
- **Cascade expand/collapse** — add an element with its full required-child chain, or remove an element and clean up orphaned descendants, with diff preview.
- **New Profile wizard** — `AKN: New Profile` command with document-type picker and snippet scaffold with tab stops.
- **Auto-install** — automatic creation of a managed Python virtual environment and installation of the language server on first activation.
- **Cross-platform support** — Windows, macOS, and Linux platform-aware venv paths.
- **Robust error handling** — safe wrappers on all LSP feature handlers to prevent single-document errors from breaking the extension.
- **esbuild bundling** — production builds are bundled and minified for fast activation and small VSIX size.

### Infrastructure

- Added `.vscodeignore` to exclude dev/test files from the VSIX package.
- Narrowed activation events to `onLanguage:akn-profile` and `workspaceContains:**/*.akn.yaml`.
- Added `@vscode/vsce` and `esbuild` as dev dependencies.
- Applied `ruff` auto-fixes across the Python codebase.

[0.1.1]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.1
[0.1.0]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.0
