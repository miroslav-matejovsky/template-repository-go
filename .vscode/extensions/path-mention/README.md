# Path Mention

Local VS Code extension. In an untitled document (new unsaved buffer, e.g. from `Ctrl+N`), typing `@` opens a list of workspace files.

- `@` triggers only at line start or after whitespace, so e-mail addresses do not trigger it.
- Text typed after `@` fuzzy-filters on the workspace-relative path, like `Ctrl+P`.
- Accepting inserts the relative path after `@`, e.g. `@internal/app/main.go`.
- Files hidden by `files.exclude` or `search.exclude` are not listed. At most 20000 files are listed.
- `Ctrl+Space` right after an `@path` reopens the list.

## Files

- `extension.js` - VS Code glue: completion provider for the `untitled` scheme.
- `mention.js` - pure logic: finding the `@` mention before the cursor, building the exclude glob.
- `mention.test.js` - unit tests for `mention.js` (`node --test`).
- `install.ps1` - links this folder into `~/.vscode/extensions`.

## Tasks

- `task vscode-ext-test` - run unit tests.
- `task vscode-ext-install` - install (junction), then run `Developer: Reload Window`.
