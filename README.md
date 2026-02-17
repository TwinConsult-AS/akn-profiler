# AKN Profiler

Author [YAML application profiles](http://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) that restrict the Akoma Ntoso 3.0 XSD — defining which elements, attributes, children, and cardinalities a jurisdiction or use-case allows.

![Overview](images/overview.png)

## Features

### New Profile Wizard

Run `AKN Profiler: New Profile` from the command palette, pick a document type, and get a complete skeleton with every required element, attribute, and cardinality pre-filled — ready to edit.

![New Profile wizard](images/new-profile-wizard.png)

### Autocomplete

Suggestions are context-aware at every level of the profile: element names, attributes, children, document types, enum values, cardinality, structure entries, and choice branches. Only valid options for the current XSD position are offered.

![Autocomplete](images/autocomplete.png)

### Inline Diagnostics

Six validation rule modules run as you type — vocabulary, structure, data types, identity, strictness, and choice groups. Errors and warnings appear inline with clear messages explaining what's wrong and how to fix it.

![Diagnostics](images/diagnostics.png)

### Hover Documentation

Hover over any element, attribute, profile key, or cardinality value to see documentation pulled from the XSD. Choice groups show an "Either/or" summary of the available branches.

![Hover](images/hover.png)

### Quick Fixes & Lightbulbs

Diagnostics come with one-click fixes — typo correction, scaffold insertion, cascade add for missing required elements. Lightbulb actions let you add or remove children, attributes, values, structure entries, and choice branches from any scope.

![Code actions](images/code-actions.png)

### And More

- **Cascade expand / collapse** — add an element with its full required-child chain, or remove one and clean up orphans, with diff preview
- **Reorder Profile** — `AKN Profiler: Reorder Profile` command sorts elements topologically (parents before children, alphabetical tiebreaking), children by XSD sequence order, and attributes by XSD field order
- **Identity attribute management** — `Add Identity Attributes` and `Remove Identity Attributes` commands to batch-add or batch-remove `eId`, `wId`, and `GUID` across the entire profile; per-attribute auto-add settings for automatic inclusion on new elements
- **Profile notes** — annotate elements with `profileNote:` for design rationale, local terminology, or usage context
- **Choice groups** — `choice:` blocks for mutually exclusive child branches, validated and cross-checked against `children:`
- **Semantic highlighting** — distinct token colors for element names (teal), attribute names (yellow), structural keywords (pink), enum values (brown), child/choice references (light blue), cardinality (green), and booleans (blue bold)
- **Code lens** — one-click "Initialize Profile Scaffold" on empty `.akn.yaml` files

## Requirements

- **Python** ≥ 3.10 (on `PATH`, or set `aknProfiler.server.pythonPath`)
- **VS Code** ≥ 1.85

The extension automatically creates a `.venv` and installs the language server on first activation — no manual `pip install` needed.

## Extension Settings

| Setting | Default | Description |
|---|---|---|
| `aknProfiler.server.pythonPath` | `"python"` | Python interpreter used to run the language server |
| `aknProfiler.identity.autoAddEId` | `true` | Automatically include `eId` on elements that support it when expanding or creating elements |
| `aknProfiler.identity.autoAddWId` | `true` | Automatically include `wId` on elements that support it when expanding or creating elements |
| `aknProfiler.identity.autoAddGUID` | `false` | Automatically include `GUID` on elements that support it when expanding or creating elements |
| `aknProfiler.identity.defaultRequired` | `true` | Default value for the `required` field when auto-adding identity attributes (eId, wId, GUID). When true, auto-added identity attributes are marked as required |

## Known Issues

No known issues. If you encounter a problem, please [open an issue](https://github.com/TwinConsult-AS/akn-profiler/issues).

## Release Notes

### 0.1.6

Fixed spurious double-quotes around cardinality values in autocomplete and profile generation output. `meta: "1..1"` is now `meta: 1..1`, consistent with cascade expand and code-action output.

### 0.1.5

Identity settings (`autoAddEId`, `autoAddWId`, `autoAddGUID`, `defaultRequired`) now apply immediately without restarting the extension. Removed the no-op `aknProfiler.schema.version` setting.

### 0.1.4

Added "Reorder Profile" command for canonical element/child/attribute ordering, "Add/Remove Identity Attributes" commands with required/optional picker for eId/wId/GUID, per-attribute auto-add settings (defaulting to true for eId/wId), `defaultRequired` setting, canonical element placement on quick-fix define, and fixed duplicate "AKN" prefix in command palette names. The "New Profile" command now generates a full minimal viable profile (matching the scaffold button) instead of a bare skeleton.

### 0.1.3

Fixed three bugs: nested choice parsing for `authorialNote` and similar elements, attribute hover now shows XSD documentation, and removed spurious blue diagnostic on custom enum values for free-typed attributes.

### 0.1.2

Added `profileNote` for curator annotations on elements — lightbulb action, completion, hover, and semantic highlighting. Fixed semantic token coloring so attribute names, choice branches, and booleans each get distinct colors.

### 0.1.1

Added XSD choice group support — `choice:` blocks, cross-block exclusion, choice validation rules, hover documentation, and auto-suggest chaining.

### 0.1.0

Initial release — autocomplete, diagnostics, hover, code actions, cascade expand/collapse, semantic highlighting, code lens, and New Profile wizard.

See the full [CHANGELOG](CHANGELOG.md) for details.

---

## Contributing

For development setup, project structure, and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).
