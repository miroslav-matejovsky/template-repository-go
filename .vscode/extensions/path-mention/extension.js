// VS Code glue for "@" path mentions in untitled (unsaved, new) documents.
//
// Typing "@" opens the suggest widget with all workspace files. Text typed after "@" fuzzy-filters
// on the workspace-relative path, like Ctrl+P. Accepting inserts the relative path after "@".
// Files are listed on every request (no cache), honoring files.exclude and search.exclude.

"use strict";

const vscode = require("vscode");
const path = require("path");
const { findMention, excludeGlob } = require("./mention");

// Upper bound on listed files so huge workspaces do not stall the suggest widget.
const MAX_FILES = 20000;

/** @param {vscode.ExtensionContext} context */
function activate(context) {
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider({ scheme: "untitled" }, { provideCompletionItems }, "@"),
  );
}

function deactivate() {}

/**
 * @param {vscode.TextDocument} document
 * @param {vscode.Position} position
 * @param {vscode.CancellationToken} token
 */
async function provideCompletionItems(document, position, token) {
  const before = document.lineAt(position.line).text.slice(0, position.character);
  const mention = findMention(before);
  if (!mention) return undefined;

  const exclude = excludeGlob(
    vscode.workspace.getConfiguration("files").get("exclude"),
    vscode.workspace.getConfiguration("search").get("exclude"),
  );
  const uris = await vscode.workspace.findFiles("**/*", exclude, MAX_FILES, token);

  // The range covers the text after "@", so VS Code filters on it and replaces it on accept.
  const range = new vscode.Range(position.line, mention.start, position.line, position.character);
  const items = uris.map((uri) => {
    const rel = vscode.workspace.asRelativePath(uri);
    const dir = path.posix.dirname(rel);
    const item = new vscode.CompletionItem(
      { label: path.posix.basename(rel), description: dir === "." ? "" : dir },
      vscode.CompletionItemKind.File,
    );
    item.filterText = rel;
    item.insertText = rel;
    item.sortText = rel;
    item.range = range;
    return item;
  });
  return new vscode.CompletionList(items, uris.length >= MAX_FILES);
}

module.exports = { activate, deactivate };
