/**
 * AKN Profiler — VS Code Language Client
 *
 * This module is the entry point for the VS Code extension. It launches
 * the Python-based language server (pygls) and connects to it over stdio
 * using the Language Server Protocol (LSP).
 *
 * Responsibilities:
 *   - Resolve the Python interpreter path from settings
 *   - Auto-install the Python language server into a managed .venv
 *   - Spawn the Python language server as a child process
 *   - Register the language client for .akn.yaml / .akn.yml files
 *   - Relay LSP messages (completion, diagnostics, hover, etc.)
 *   - Register "AKN: New Profile" command
 *   - Auto-generate scaffold for empty .akn.yaml files
 */

import * as path from "path";
import * as fs from "fs";
import { execFile } from "child_process";
import { promisify } from "util";
import {
  commands,
  ExtensionContext,
  Position as VPosition,
  ProgressLocation,
  Range,
  Selection,
  SnippetString,
  TextDocument,
  Uri,
  workspace,
  window,
  OutputChannel,
} from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
} from "vscode-languageclient/node";

const execFileAsync = promisify(execFile);

let client: LanguageClient | undefined;
let outputChannel: OutputChannel;

// ------------------------------------------------------------------
// Platform-aware helpers
// ------------------------------------------------------------------

/** Return the correct venv Python path for the current platform. */
function venvPythonPath(venvDir: string): string {
  if (process.platform === "win32") {
    return path.join(venvDir, "Scripts", "python.exe");
  }
  return path.join(venvDir, "bin", "python");
}

/**
 * Ensure the Python language server is installed in a managed .venv.
 * Returns the resolved Python interpreter path.
 */
async function ensureServerInstalled(
  context: ExtensionContext,
  systemPython: string,
): Promise<string> {
  const venvDir = path.join(context.extensionPath, ".venv");
  const venvPython = venvPythonPath(venvDir);
  const markerFile = path.join(venvDir, ".akn-server-installed");

  // Fast path: server is already installed
  if (fs.existsSync(markerFile) && fs.existsSync(venvPython)) {
    outputChannel.appendLine(`Server already installed (marker: ${markerFile})`);
    return venvPython;
  }

  // Check if *any* Python >= 3.10 is available
  try {
    const { stdout } = await execFileAsync(systemPython, [
      "-c",
      "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
    ]);
    const [major, minor] = stdout.trim().split(".").map(Number);
    if (major < 3 || (major === 3 && minor < 10)) {
      const msg = `Python ${stdout.trim()} found but Python >= 3.10 is required.`;
      outputChannel.appendLine(msg);
      const action = await window.showErrorMessage(
        msg,
        "Set Python Path",
      );
      if (action === "Set Python Path") {
        await commands.executeCommand("workbench.action.openSettings", "aknProfiler.server.pythonPath");
      }
      throw new Error(msg);
    }
  } catch (err: any) {
    if (err.code === "ENOENT" || err.message?.includes("not found")) {
      const msg = `Python interpreter not found at "${systemPython}". Install Python >= 3.10 or set aknProfiler.server.pythonPath.`;
      outputChannel.appendLine(msg);
      const action = await window.showErrorMessage(
        msg,
        "Set Python Path",
      );
      if (action === "Set Python Path") {
        await commands.executeCommand("workbench.action.openSettings", "aknProfiler.server.pythonPath");
      }
      throw new Error(msg);
    }
    throw err;
  }

  // Install with progress
  return window.withProgress(
    {
      location: ProgressLocation.Notification,
      title: "AKN Profiler",
      cancellable: false,
    },
    async (progress) => {
      // Step 1: Create venv
      if (!fs.existsSync(venvPython)) {
        progress.report({ message: "Creating Python virtual environment…" });
        outputChannel.appendLine(`Creating venv at ${venvDir}…`);
        await execFileAsync(systemPython, ["-m", "venv", venvDir]);
        outputChannel.appendLine("venv created.");
      }

      // Step 2: Install the server package
      progress.report({ message: "Installing language server…" });
      const serverDir = path.join(context.extensionPath, "server");
      outputChannel.appendLine(`Installing server from ${serverDir}…`);
      await execFileAsync(venvPython, ["-m", "pip", "install", "--upgrade", "pip"], {
        cwd: serverDir,
      });
      await execFileAsync(venvPython, ["-m", "pip", "install", "."], {
        cwd: serverDir,
        timeout: 300_000, // 5 min timeout for slow networks
      });
      outputChannel.appendLine("Server package installed.");

      // Step 3: Write marker
      fs.writeFileSync(markerFile, new Date().toISOString());
      outputChannel.appendLine("Installation marker written.");

      return venvPython;
    },
  );
}

export async function activate(context: ExtensionContext): Promise<void> {
  // Create output channel for logging
  outputChannel = window.createOutputChannel("AKN Profiler");
  outputChannel.appendLine("AKN Profiler extension activating...");

  // Register commands eagerly so they are available even if server fails
  registerNewProfileCommand(context);
  registerScaffoldCommand(context);
  registerCascadeCommands(context);
  registerCursorToLineCommand(context);

  // Resolve Python interpreter path from settings
  const config = workspace.getConfiguration("aknProfiler");
  let pythonPath = config.get<string>("server.pythonPath", "python");

  // Resolve ${workspaceFolder} variable
  if (pythonPath.includes("${workspaceFolder}")) {
    const wsFolder = workspace.workspaceFolders?.[0]?.uri.fsPath ?? context.extensionPath;
    pythonPath = pythonPath.replace("${workspaceFolder}", wsFolder);
  }

  outputChannel.appendLine(`Configured Python path: ${pythonPath}`);
  outputChannel.appendLine(`Extension path: ${context.extensionPath}`);

  // Auto-install the server into a managed venv
  let resolvedPython: string;
  try {
    resolvedPython = await ensureServerInstalled(context, pythonPath);
  } catch (err: any) {
    outputChannel.appendLine(`Server installation failed: ${err.message}`);
    return; // Error already shown to user
  }

  outputChannel.appendLine(`Resolved Python: ${resolvedPython}`);

  // Build ServerOptions to spawn the Python language server
  const serverOptions: ServerOptions = {
    command: resolvedPython,
    args: ["-m", "akn_profiler"],
    options: {
      cwd: context.extensionPath,
      env: {
        ...process.env,
        PYTHONPATH: path.join(context.extensionPath, "server"),
      },
    },
  };

  outputChannel.appendLine(`Server command: ${resolvedPython} -m akn_profiler`);

  // Build LanguageClientOptions for .akn.yaml documents
  const schemaVersion = workspace.getConfiguration("aknProfiler").get<string>("schema.version", "3.0");
  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: "file", language: "akn-profile" },
      { scheme: "file", pattern: "**/*.akn.{yaml,yml}" },
      { scheme: "untitled", language: "akn-profile" },
    ],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher("**/*.akn.{yaml,yml}"),
    },
    outputChannel: outputChannel,
    initializationOptions: {
      schemaVersion,
    },
  };

  // Create and start the LanguageClient
  client = new LanguageClient(
    "aknProfiler",
    "AKN Profiler Language Server",
    serverOptions,
    clientOptions
  );

  outputChannel.appendLine("Starting language client...");

  // Start the client (this also launches the server)
  client
    .start()
    .then(() => {
      outputChannel.appendLine("✅ Language server started successfully");
    })
    .catch((error) => {
      outputChannel.appendLine(`❌ Error starting language server: ${error}`);
      outputChannel.appendLine(`Stack: ${error.stack}`);
      window.showErrorMessage(
        `Failed to start AKN Profiler language server: ${error.message}`
      );
      console.error("Language server error:", error);
    });

  context.subscriptions.push(client, outputChannel);
}

// ------------------------------------------------------------------
// "Initialize Profile Scaffold" CodeLens command
// ------------------------------------------------------------------

function registerScaffoldCommand(context: ExtensionContext): void {
  const disposable = commands.registerCommand(
    "akn-profiler.insertScaffold",
    async () => {
      if (!client) {
        window.showErrorMessage("AKN Profiler language server is not running.");
        return;
      }

      const editor = window.activeTextEditor;
      if (!editor) {
        return;
      }

      // Ask the server for valid document types
      let docTypes: string[];
      try {
        // Ensure the server is ready before making the request
        if (!client.isRunning()) {
          await client.start();
        }
        docTypes = await client.sendRequest(
          "workspace/executeCommand",
          { command: "akn.documentTypes", arguments: [] }
        );
      } catch (err) {
        outputChannel.appendLine(`insertScaffold: failed to get document types: ${err}`);
        window.showErrorMessage("Could not retrieve document types from the server.");
        return;
      }

      if (!docTypes || docTypes.length === 0) {
        window.showWarningMessage("No document types available.");
        return;
      }

      const selected = await window.showQuickPick(docTypes, {
        placeHolder: "Select an AKN document type",
        title: "Initialize Profile Scaffold",
      });

      if (!selected) {
        return; // User cancelled
      }

      // Ask the server to build a full minimal profile with recursive expansion
      let fullProfile: string;
      try {
        fullProfile = await client.sendRequest(
          "workspace/executeCommand",
          { command: "akn.initializeProfile", arguments: [selected] }
        );
      } catch (err) {
        outputChannel.appendLine(`insertScaffold: failed to initialize profile: ${err}`);
        window.showErrorMessage("Could not generate profile scaffold.");
        return;
      }

      if (!fullProfile) {
        window.showWarningMessage("Server returned empty profile.");
        return;
      }

      const lastLine = editor.document.lineCount - 1;
      const fullRange = new Range(
        new VPosition(0, 0),
        editor.document.lineAt(lastLine).range.end
      );

      await editor.edit((editBuilder) => {
        editBuilder.replace(fullRange, fullProfile);
      });

      // Position cursor at the name value so the user can fill in metadata
      const pos = new VPosition(1, 9); // after '  name: "'
      editor.selection = new Selection(pos, pos);
      editor.revealRange(editor.selection);

      outputChannel.appendLine(
        `Profile scaffold initialized with document type: ${selected}`
      );
    }
  );

  context.subscriptions.push(disposable);
  outputChannel.appendLine('Registered command: "akn-profiler.insertScaffold"');
}

// ------------------------------------------------------------------
// "AKN: New Profile" command
// ------------------------------------------------------------------

function registerNewProfileCommand(context: ExtensionContext): void {
  const disposable = commands.registerCommand(
    "akn-profiler.newProfile",
    async () => {
      if (!client) {
        window.showErrorMessage("AKN Profiler language server is not running.");
        return;
      }

      try {
        // Ask the server for valid document types
        const docTypes: string[] = await client.sendRequest(
          "workspace/executeCommand",
          { command: "akn.documentTypes", arguments: [] }
        );

        if (!docTypes || docTypes.length === 0) {
          window.showWarningMessage(
            "Could not retrieve document types from the server."
          );
          return;
        }

        // Show quick pick
        const selected = await window.showQuickPick(docTypes, {
          placeHolder: "Select an AKN document type for the new profile",
          title: "New AKN Profile",
        });

        if (!selected) {
          return; // User cancelled
        }

        // Ask the server for the snippet scaffold
        const snippet: string = await client.sendRequest(
          "workspace/executeCommand",
          { command: "akn.generateSnippet", arguments: [selected] }
        );

        if (!snippet) {
          window.showWarningMessage("Could not generate profile scaffold.");
          return;
        }

        // Open a new untitled document with the akn-profile language
        const doc = await workspace.openTextDocument({
          language: "akn-profile",
          content: "",
        });
        const editor = await window.showTextDocument(doc);

        // Insert the snippet (with tab-stop support)
        await editor.insertSnippet(new SnippetString(snippet));

        outputChannel.appendLine(
          `New profile created for document type: ${selected}`
        );
      } catch (err) {
        outputChannel.appendLine(`Error creating new profile: ${err}`);
        window.showErrorMessage(`Failed to create profile: ${err}`);
      }
    }
  );

  context.subscriptions.push(disposable);
  outputChannel.appendLine('Registered command: "AKN: New Profile"');
}

// ------------------------------------------------------------------
// Cascade add/remove with diff preview
// ------------------------------------------------------------------

function registerCascadeCommands(context: ExtensionContext): void {
  // Cascade Add (expand element + required children)
  const expandDisposable = commands.registerCommand(
    "akn-profiler.expandElement",
    async () => {
      if (!client) {
        window.showErrorMessage("AKN Profiler language server is not running.");
        return;
      }

      const editor = window.activeTextEditor;
      if (!editor || !isAknProfile(editor.document)) {
        window.showWarningMessage("Open an .akn.yaml file first.");
        return;
      }

      // Ask user which element to add
      const elemName = await window.showInputBox({
        prompt: "Element name to add (cascades into required children)",
        placeHolder: "e.g. act, meta, body",
      });
      if (!elemName) {
        return;
      }

      try {
        const result: { newText: string } = await client.sendRequest(
          "workspace/executeCommand",
          {
            command: "akn.expandElement",
            arguments: [editor.document.uri.toString(), elemName],
          }
        );

        if (!result?.newText) {
          window.showWarningMessage("No changes needed.");
          return;
        }

        // Show diff preview
        await showDiffPreview(editor.document, result.newText, `Add "${elemName}" (cascade)`);
      } catch (err) {
        outputChannel.appendLine(`Cascade expand error: ${err}`);
        window.showErrorMessage(`Failed to expand element: ${err}`);
      }
    }
  );

  // Cascade Remove (collapse element + orphan cleanup)
  const collapseDisposable = commands.registerCommand(
    "akn-profiler.collapseElement",
    async () => {
      if (!client) {
        window.showErrorMessage("AKN Profiler language server is not running.");
        return;
      }

      const editor = window.activeTextEditor;
      if (!editor || !isAknProfile(editor.document)) {
        window.showWarningMessage("Open an .akn.yaml file first.");
        return;
      }

      // Ask user which element to remove
      const elemName = await window.showInputBox({
        prompt: "Element name to remove (cleans up orphaned descendants)",
        placeHolder: "e.g. body, meta",
      });
      if (!elemName) {
        return;
      }

      try {
        const result: { newText: string } = await client.sendRequest(
          "workspace/executeCommand",
          {
            command: "akn.collapseElement",
            arguments: [editor.document.uri.toString(), elemName],
          }
        );

        if (!result?.newText) {
          window.showWarningMessage("No changes needed.");
          return;
        }

        // Show diff preview
        await showDiffPreview(editor.document, result.newText, `Remove "${elemName}" (cascade)`);
      } catch (err) {
        outputChannel.appendLine(`Cascade collapse error: ${err}`);
        window.showErrorMessage(`Failed to remove element: ${err}`);
      }
    }
  );

  context.subscriptions.push(expandDisposable, collapseDisposable);
  outputChannel.appendLine("Registered cascade add/remove commands.");
}

// ------------------------------------------------------------------
// Cursor positioning command (used by Code Action "Add …" lightbulbs)
// ------------------------------------------------------------------

function registerCursorToLineCommand(context: ExtensionContext): void {
  const disposable = commands.registerCommand(
    "akn-profiler.cursorToLine",
    async (line: number, character: number) => {
      const editor = window.activeTextEditor;
      if (!editor) {
        return;
      }

      // Clamp to valid range
      const targetLine = Math.min(line, editor.document.lineCount - 1);
      const targetChar = Math.max(0, character);

      const pos = new VPosition(targetLine, targetChar);
      editor.selection = new Selection(pos, pos);
      editor.revealRange(editor.selection);

      // Trigger the completion menu so the user can pick a value
      await commands.executeCommand("editor.action.triggerSuggest");
    }
  );

  context.subscriptions.push(disposable);
  outputChannel.appendLine('Registered command: "akn-profiler.cursorToLine"');
}

async function showDiffPreview(
  originalDoc: TextDocument,
  newText: string,
  title: string
): Promise<void> {
  // Create a virtual document with the new content
  const originalUri = originalDoc.uri;
  const previewUri = Uri.parse(
    `untitled:${originalUri.fsPath}.preview.akn.yaml`
  );

  // Open a new document with the proposed changes
  const previewDoc = await workspace.openTextDocument({
    content: newText,
    language: "akn-profile",
  });

  // Use the built-in diff editor
  await commands.executeCommand(
    "vscode.diff",
    originalUri,
    previewDoc.uri,
    `${title} — Preview changes`
  );
}

function isAknProfile(doc: TextDocument): boolean {
  if (doc.languageId === "akn-profile") {
    return true;
  }
  const name = doc.fileName.toLowerCase();
  return name.endsWith(".akn.yaml") || name.endsWith(".akn.yml");
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  outputChannel?.appendLine("Stopping language client...");
  return client.stop();
}
