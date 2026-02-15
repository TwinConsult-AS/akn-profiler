# Contributing to AKN Profiler

## Prerequisites

- **Node.js** ≥ 18 and **npm** ≥ 9
- **Python** ≥ 3.10
- **VS Code** ≥ 1.85

## Getting Started

### 1. Clone & install

```bash
git clone https://github.com/TwinConsult-AS/akn-profiler.git
cd akn-profiler
npm install
```

### 2. Set up Python

```bash
cd server
python -m venv ../.venv

# Windows:
..\.venv\Scripts\activate
# macOS / Linux:
source ../.venv/bin/activate

pip install -e ".[dev]"
```

### 3. Run

Press **F5** in VS Code to launch the Extension Development Host, then open or create a `.akn.yaml` file.

### 4. Test

```bash
# TypeScript compile check
npm run compile

# Python tests
cd server
pytest -v
```

## Project Structure

```
akn-profiler/
├── client/                    # TypeScript — VS Code Language Client
│   ├── src/
│   │   └── extension.ts       # Extension entry point (activate/deactivate)
│   ├── package.json
│   └── tsconfig.json
│
├── server/                    # Python — Language Server (pygls)
│   ├── akn_profiler/
│   │   ├── __main__.py        # python -m akn_profiler entry point
│   │   ├── server.py          # LanguageServer & all feature handlers
│   │   ├── models/
│   │   │   ├── cascade.py     # Cascade expand/collapse operations
│   │   │   ├── generator.py   # Minimum viable profile generator
│   │   │   ├── profile.py     # Pydantic models for .akn.yaml profiles
│   │   │   └── snippet_generator.py
│   │   ├── xsd/
│   │   │   ├── choice_parser.py  # XSD choice/group parser
│   │   │   ├── generated.py   # xsdata-generated AKN dataclasses
│   │   │   └── schema_loader.py  # Queryable schema representation
│   │   └── validation/
│   │       ├── engine.py      # Validation orchestrator
│   │       ├── errors.py
│   │       ├── rules_choice.py
│   │       ├── rules_datatype.py
│   │       ├── rules_identity.py
│   │       ├── rules_strictness.py
│   │       ├── rules_structure.py
│   │       ├── rules_vocabulary.py
│   │       ├── yaml_context.py
│   │       └── yaml_parser.py
│   ├── tests/                 # pytest suite (250+ tests)
│   └── pyproject.toml
│
├── schemas/
│   ├── akomantoso30.xsd       # AKN 3.0 schema (OASIS Standard)
│   └── xml.xsd
│
├── syntaxes/
│   └── akn-profile.tmLanguage.json  # TextMate grammar
│
├── package.json               # VS Code extension manifest
├── esbuild.mjs                # Bundler configuration
├── language-configuration.json
└── CHANGELOG.md
```

## Architecture

The extension uses a **client–server** architecture over the Language Server Protocol (LSP):

- **Client** (`client/`) — TypeScript. Spawns the Python server, relays LSP messages, registers VS Code commands.
- **Server** (`server/`) — Python ([pygls](https://github.com/openlawlibrary/pygls)). Loads the AKN 3.0 XSD, builds [Pydantic](https://docs.pydantic.dev/) models, and implements all language features (completions, diagnostics, hover, code actions, semantic tokens, code lens).

Communication is over stdio using JSON-RPC.

## Akoma Ntoso Background

[Akoma Ntoso](http://www.akomantoso.org/) ("linked hearts" in Akan) is an OASIS Standard XML vocabulary for parliamentary, legislative, and judicial documents. The AKN 3.0 XSD defines ~310 element names and ~69 attribute names across 7 document types. An **application profile** restricts this broad schema to a specific jurisdiction — for example, "Norwegian parliamentary bills must use chapters > articles > paragraphs."
