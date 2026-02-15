# AKN Profiler

A Visual Studio Code extension for authoring **YAML application profiles** that restrict the [Akoma Ntoso (AKN) 3.0](http://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) XML schema. It provides autocomplete, inline suggestions, validation, and automatic generation of minimum-viable profile skeletons — all powered by Pydantic models derived from the official AKN XSD.

---

## Features

| Feature | Description |
|---|---|
| **Auto-generate profile** | Create a minimum-viable `.akn.yaml` skeleton for any AKN document type |
| **Autocomplete** | Context-aware suggestions for AKN elements, attributes, and restriction values |
| **Inline diagnostics** | Real-time validation that profile restrictions conform to the AKN schema |
| **Hover documentation** | Inline docs for AKN elements pulled from the XSD annotations |
| **Quick-fix actions** | Code actions to correct invalid restrictions |
| **Add / Remove lightbulbs** | Contextual lightbulb actions to add children, attributes, values, and structure entries |
| **Cascade expand / collapse** | Add an element with its full required-child chain, or remove an element and clean up orphans, with diff preview |
| **Code lens** | "Initialize Profile Scaffold" button on empty files |
| **Semantic highlighting** | Distinct colors for elements, attributes, keywords, enum values, children, and cardinality |
| **Inlay hints** | Ghost-text cardinality hints (e.g. `1..1`, `0..*`) after element and child keys |
| **New Profile wizard** | `AKN: New Profile` command with document-type picker and snippet scaffold |
| **Snippet generation** | VS Code snippet scaffolds for any AKN document type |

---

## Architecture

The extension follows a **client–server** architecture using the [Language Server Protocol (LSP)](https://microsoft.github.io/language-server-protocol/):

```
┌──────────────────────────────────────────────────────────┐
│  VS Code                                                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │  TypeScript Language Client  (client/)             │  │
│  │  • Spawns & manages the Python server process      │  │
│  │  • Relays LSP messages (completion, diagnostics…)  │  │
│  └──────────────┬─────────────────────────────────────┘  │
│                 │  stdio (JSON-RPC)                       │
│  ┌──────────────▼─────────────────────────────────────┐  │
│  │  Python Language Server  (server/)                 │  │
│  │  ┌───────────┐  ┌──────────┐  ┌────────────────┐  │  │
│  │  │  pygls     │  │ Pydantic │  │  xsdata        │  │  │
│  │  │  LSP core  │  │ Models   │  │  XSD parsing   │  │  │
│  │  └───────────┘  └──────────┘  └────────────────┘  │  │
│  │                      │                             │  │
│  │              ┌───────▼───────┐                     │  │
│  │              │  Validation   │                     │  │
│  │              │  Engine       │                     │  │
│  │              └───────────────┘                     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                          │
                ┌─────────▼─────────┐
                │  schemas/         │
                │  akomantoso30.xsd │
                │  xml.xsd          │
                └───────────────────┘
```

### Data Flow

1. **At startup** — the Python server loads `schemas/akomantoso30.xsd`, parses it with **xsdata**, and builds **Pydantic** models representing every AKN element, attribute, type, and constraint.
2. **On file open/edit** — the user's `.akn.yaml` profile is deserialised and validated against the Pydantic models. Diagnostics (errors/warnings) are pushed to VS Code.
3. **On completion request** — the server inspects the cursor position in the YAML, determines which AKN schema node is being restricted, and returns valid options.
4. **On new-file** — a minimum-viable profile skeleton is auto-generated containing required elements and default restrictions.

---

## Project Structure

```
akn-profiler/
├── .vscode/
│   ├── launch.json            # Debug configurations (Client + Server)
│   ├── tasks.json             # Build & test tasks
│   ├── settings.json          # Workspace settings
│   └── extensions.json        # Recommended extensions
│
├── client/                    # TypeScript — VS Code Language Client
│   ├── src/
│   │   └── extension.ts       # Extension entry point (activate/deactivate)
│   ├── package.json           # Client dependencies (vscode-languageclient)
│   └── tsconfig.json
│
├── server/                    # Python — Language Server
│   ├── akn_profiler/
│   │   ├── __init__.py
│   │   ├── __main__.py        # `python -m akn_profiler` entry point
│   │   ├── server.py          # pygls LanguageServer setup & feature handlers
│   │   ├── models/            # Pydantic BaseModel classes for AKN & profiles
│   │   │   └── __init__.py
│   │   ├── xsd/               # XSD schema loading & xsdata bindings
│   │   │   └── __init__.py
│   │   └── validation/        # Profile validation against AKN schema
│   │       └── __init__.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_cascade.py
│   │   ├── test_code_actions_add.py
│   │   ├── test_code_lens.py
│   │   ├── test_completion.py
│   │   ├── test_engine.py
│   │   ├── test_generator.py
│   │   ├── test_placeholder.py
│   │   ├── test_rules_datatype.py
│   │   ├── test_rules_identity.py
│   │   ├── test_rules_strictness.py
│   │   ├── test_rules_structure.py
│   │   ├── test_rules_vocabulary.py
│   │   ├── test_schema_loader.py
│   │   ├── test_snippet_generator.py
│   │   ├── test_yaml_context.py
│   │   └── test_yaml_parser.py
│   └── pyproject.toml         # Python project config & dependencies
│
├── schemas/                   # Official Akoma Ntoso XSD (source of truth)
│   ├── akomantoso30.xsd       # AKN 3.0 main schema (OASIS Standard)
│   └── xml.xsd                # XML namespace support schema
│
├── package.json               # Root VS Code extension manifest
├── tsconfig.json              # Root TypeScript project references
├── esbuild.mjs                # esbuild bundler configuration
├── language-configuration.json
├── .vscodeignore              # Files excluded from VSIX packaging
├── CHANGELOG.md
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation

### From the Marketplace (recommended)

1. Open VS Code.
2. Go to **Extensions** (Ctrl+Shift+X).
3. Search for **AKN Profiler**.
4. Click **Install**.

The extension will automatically create a Python virtual environment and install the language server on first activation.

### From VSIX

```bash
code --install-extension akn-profiler-0.1.0.vsix
```

### Requirements

- **Python** ≥ 3.10 (must be available on `PATH` or configured via `aknProfiler.server.pythonPath`)
- **VS Code** ≥ 1.85

The extension automatically manages a `.venv` with all Python dependencies — no manual `pip install` is needed for end users.

---

## Configuration

| Setting | Default | Description |
|---|---|---|
| `aknProfiler.server.pythonPath` | `"python"` | Path to the Python interpreter used to run the language server |
| `aknProfiler.schema.version` | `"3.0"` | Akoma Ntoso schema version (currently only 3.0 is supported) |

---

## Development

### Prerequisites

- **Node.js** ≥ 18 and **npm** ≥ 9
- **Python** ≥ 3.10
- **VS Code** ≥ 1.85

### 1. Clone & install Node dependencies

```bash
git clone https://github.com/TwinConsult-AS/akn-profiler.git
cd akn-profiler
npm install          # installs root devDeps + runs postinstall for client/
```

### 2. Set up the Python environment

```bash
cd server
python -m venv ../.venv        # or use an existing venv
# Windows:
..\.venv\Scripts\activate
# macOS / Linux:
source ../.venv/bin/activate

pip install -e ".[dev]"        # install server package in editable mode with dev extras
```

### 3. Launch the Extension Development Host

1. Open the workspace in VS Code.
2. Press **F5** (or run the **Launch Extension (Client)** configuration).
3. In the new Extension Development Host window, open or create a `.akn.yaml` file.

---

## Key Technologies

| Layer | Technology | Role |
|---|---|---|
| **Editor integration** | [VS Code Extension API](https://code.visualstudio.com/api) | Extension host, activation, settings |
| **Client ↔ Server** | [LSP](https://microsoft.github.io/language-server-protocol/) via [vscode-languageclient](https://github.com/microsoft/vscode-languageserver-node) | Completion, diagnostics, hover, code actions |
| **Server framework** | [pygls](https://github.com/openlawlibrary/pygls) | Python LSP server implementation |
| **Schema parsing** | [xsdata](https://github.com/tefra/xsdata) | XSD → Python dataclass generation & XML binding |
| **Data modelling** | [Pydantic v2](https://docs.pydantic.dev/) | Typed models, validation, JSON Schema export |
| **XML processing** | [lxml](https://lxml.de/) | Fast XML/XSD parsing backend |
| **Profile format** | YAML (`.akn.yaml`) | Human-friendly application profile authoring |

---

## Akoma Ntoso Background

[Akoma Ntoso](http://www.akomantoso.org/) ("linked hearts" in Akan) is an OASIS Standard XML vocabulary for parliamentary, legislative, and judicial documents. The AKN 3.0 schema defines ~310 element names and ~69 attribute names covering:

- **7 document types** — act, bill, debate, judgment, amendment, doc, debateReport
- **Hierarchical structures** — book, part, title, chapter, article, section, paragraph…
- **Metadata** — FRBR identification, lifecycle, classification, references
- **Modifications & versioning** — active/passive modifications, temporal data

An **application profile** restricts this broad schema to a specific jurisdiction or use-case — for example, "Norwegian parliamentary bills must have chapters > articles > paragraphs, and the `language` attribute is required on `<akomaNtoso>`."

---

## License

See [LICENSE](LICENSE).
