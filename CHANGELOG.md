# Changelog

All notable changes to the AKN Profiler extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-02-15

### Added

- **Language support** for `.akn.yaml` / `.akn.yml` files with TextMate grammar and semantic highlighting.
- **Auto-completion** — context-aware suggestions for profile keys, AKN element names, attribute names, document types, enum values, children, and structure entries.
- **Inline diagnostics** — real-time validation engine with rule modules for vocabulary, structure, data types, identity, and strictness.
- **Hover documentation** — XSD-sourced documentation for AKN elements, attributes, profile keys, and cardinality.
- **Code actions** — diagnostic-based quick-fixes (typo correction, scaffold insertion) and contextual "Add …" lightbulb actions for children, attributes, and values.
- **Code lens** — "Initialize Profile Scaffold" button on empty `.akn.yaml` files.
- **Semantic tokens** — full semantic highlighting for element names, attributes, keywords, enum values, child references, cardinality, and booleans.
- **Inlay hints** — ghost-text cardinality hints (e.g. `1..1`, `0..*`) after element and child keys.
- **Cascade expand/collapse** — add an element with its full required-child chain, or remove an element and clean up orphaned descendants, with diff preview.
- **New Profile wizard** — `AKN: New Profile` command with document-type picker and snippet scaffold with tab stops.
- **Snippet generation** — VS Code snippet scaffolds for any AKN document type.
- **Auto-install** — automatic creation of a managed Python virtual environment and installation of the language server on first activation.
- **Cross-platform support** — Windows, macOS, and Linux platform-aware venv paths.
- **Robust error handling** — safe wrappers on all LSP feature handlers to prevent single-document errors from breaking the extension.
- **esbuild bundling** — production builds are bundled and minified for fast activation and small VSIX size.

### Infrastructure

- Added `.vscodeignore` to exclude dev/test files from the VSIX package.
- Narrowed activation events to `onLanguage:akn-profile` and `workspaceContains:**/*.akn.yaml`.
- Added `@vscode/vsce` and `esbuild` as dev dependencies.
- Applied `ruff` auto-fixes across the Python codebase.

[0.1.0]: https://github.com/TwinConsult-AS/akn-profiler/releases/tag/v0.1.0
