# Testing the AKN Profiler Extension

## Quick Start

1. **Press F5** in VS Code to launch the Extension Development Host
2. In the new window, **create** a new file called `test.akn.yaml` (leave it empty)
3. Check the **Output** panel (View → Output) and select "AKN Profiler Language Server" from the dropdown

## New Profile Workflow

1. Open the empty `.akn.yaml` file — a diagnostic appears: *"Profile must be a YAML mapping"*
2. Press **Ctrl+.** (or click the lightbulb) → **"Insert profile scaffold"**
3. Fill in name, version, description, and a document type (e.g. `act`)
4. A new diagnostic appears on the document type → press **Ctrl+.** → **"Define 'act' with required attributes and children"**
5. All required elements are auto-generated (act, meta, body, identification, FRBR elements, etc.)

## What to Expect

✅ **Success indicators:**
- Extension activates when opening `.akn.yaml` files
- Python language server starts (check Output panel)
- "AKN Profiler server initialized" message appears
- Lightbulb quick-fixes appear for diagnostics
- Cascade element generation works in one click

❌ **If it doesn't work:**
- Check Python path in settings: `.vscode/settings.json` → `python.defaultInterpreterPath`
- Verify dependencies: Run `pip list` in `.venv` — should see `pygls`, `pydantic`, etc.
- Check for errors in the Output panel and Debug Console

## Testing Checklist

- [ ] Extension activates on `.akn.yaml` file open
- [ ] Server starts without errors
- [ ] Empty file shows "Insert profile scaffold" lightbulb
- [ ] Scaffold insertion works correctly
- [ ] Document type triggers "Define with required elements" lightbulb
- [ ] Cascade generates all required elements
- [ ] Add/remove child lightbulbs work on element children
- [ ] No errors in Debug Console or Output panel
