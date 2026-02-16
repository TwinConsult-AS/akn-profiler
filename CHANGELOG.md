# Changelog

All notable changes to the AKN Profiler extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] — 2026-02-16

### Added

- **Reorder Profile command** — new "AKN Profiler: Reorder Profile" command (`Ctrl+Shift+P`) reorders the entire profile into canonical order: elements follow a topological parent-before-child arrangement with alphabetical tiebreaking, children within each element follow XSD sequence order (required first), and attributes follow XSD field order (required first).
- **Add Identity Attributes command** — new "AKN Profiler: Add Identity Attributes" command presents a multi-select picker for `eId`, `wId`, and `GUID`, followed by a "Required" or "Optional" picker to control the `required` field value. Selected attributes are added to every element in the profile that supports them per the XSD.
- **Remove Identity Attributes command** — symmetric command to remove identity attributes from all elements (respects XSD-required attributes — won't remove attributes that are mandatory).
- **Identity attribute auto-add settings** — four new VS Code settings: `aknProfiler.identity.autoAddEId` (default `true`), `aknProfiler.identity.autoAddWId` (default `true`), `aknProfiler.identity.autoAddGUID` (default `false`), and `aknProfiler.identity.defaultRequired` (default `true`). These control which identity attributes are automatically included when expanding elements via cascade add, scaffold initialization, or the New Profile wizard, and whether they're marked as required.
- **Canonical element ordering on expand** — when using quick-fix "Define element" or cascade add, new elements are now placed in logical topological order (parents before children, alphabetical tiebreaking) instead of being appended at the bottom.

### Changed

- **New Profile command generates full profile** — the "New Profile" wizard now produces a complete minimal viable profile with all required elements, children, and attributes, matching the "Initialize Profile Scaffold" button. Previously it only generated a bare skeleton that required manual expansion via quick-fixes.
- **Completion sort order** — children and attributes in autocomplete dropdowns continue to sort required-first then alphabetically, consistent with the new canonical ordering used throughout.

### Fixed

- **Duplicate "AKN" in command palette** — all command titles no longer include the redundant `AKN:` prefix, since the category `AKN Profiler` already provides it. Commands now display as "AKN Profiler: New Profile" instead of "AKN Profiler: AKN: New Profile".
- **Stale server version string** — `LanguageServer` version updated from `v0.1.2` to `v0.1.4`.

### Infrastructure

- Test suite expanded with new coverage for element ordering, reorder command, identity attribute add/remove, and auto-add settings.

## [0.1.3] — 2026-02-16

### Fixed

- **authorialNote choice groups** — nested `<xsd:choice>` elements in XSD complex types (e.g. `subFlowStructure`) are now correctly parsed and attached as choice group branches. Previously, `authorialNote` and similar elements showed only `documentType` as a required child, incorrectly ignoring the inner choice of block/container elements. The choice parser now handles nested choices recursively.
- **Attribute hover documentation** — hovering over an attribute name in a profile now displays the XSD documentation text extracted from the attribute group annotation (e.g. `class` → "These attributes are used to specify class, style and title of the element, exactly as in HTML"). Previously only type, pattern, and enum values were shown.
- **Removed spurious enum diagnostic** — custom `values:` lists on free-typed attributes (e.g. `class`, `style`) no longer emit a blue INFO diagnostic (`datatype.custom-enum-on-free-attribute`). Profiles tightening the schema with custom enums is normal behavior and needs no diagnostic.

### Infrastructure

- Test suite expanded to 301 tests, including new coverage for attribute documentation extraction, nested choice parsing, and updated datatype validation expectations.

## [0.1.2] — 2026-02-16

### Added

- **Profile notes** — new `profileNote` key on element entries for curator annotations (e.g. mapping to local terminology, design rationale). Informational only — does not affect validation.
- **"Add profile note" lightbulb** — code action inserts `profileNote: ""` as the first sub-key under an element and positions the cursor for typing.
- Auto-completion and hover documentation for `profileNote`.

### Fixed

- **Semantic token coloring** — attribute names under `attributes:` (e.g. `name`, `version`, `description`) now correctly render as Property (yellow) instead of Keyword (pink). Element names in `choice:` branches now render as Type (light blue) with cardinality highlighting.
- **Boolean highlighting** — `true`/`false` values on `required:` lines now render as Macro (blue bold) instead of being uncolored.
- **Hover on `profileNote`** — hovering the `profileNote` key now shows its dedicated documentation instead of the parent element's XSD doc.
- **Lightbulb scope** — "Add child", "Add attribute", and "Add profile note" lightbulbs are now visible when the cursor is on a `profileNote` line.
- **Lightbulb ordering** — code actions now appear in a consistent order: choice → children → attribute → profile note.
- **No spurious completion popup** — the "Add profile note" code action no longer triggers a completion dropdown after insertion.

### Infrastructure

- Test suite expanded to 296 tests, including 34 new semantic token tests.

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

[0.1.4]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.4
[0.1.3]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.3
[0.1.2]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.2
[0.1.1]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.1
[0.1.0]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.0
