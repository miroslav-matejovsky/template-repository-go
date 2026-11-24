# Development tooling

`mise.toml` declares tool versions, simple command tasks, and the `all` sequence.
mise automatically discovers executable Python tasks in `.mise/tasks/`; their
`#MISE` comments declare descriptions and dependencies. mise installs Go, Python,
golangci-lint, and the Go command-line tools. Python scripts use only the standard
library and work on Windows, Linux, and macOS.

## Setup and configuration

Install [mise](https://mise.jdx.dev/getting-started.html), review `mise.toml`, and run
`mise trust` followed by `mise install`. Git must be available for repository
maintenance. GitHub CLI (`gh`) must be installed and authenticated for releases.

Tool versions are explicit in `[tools]`. Keep the Go version aligned with `go.mod`.
Go command-line packages use mise's [go backend](https://mise.jdx.dev/dev-tools/backends/go.html).
golangci-lint uses its published binary. To change a tool version, edit its entry
in `mise.toml` and run `mise install`.

For private environment variables, copy `mise.local.toml.example` to
`mise.local.toml`, replace the example values, and run `mise trust` if prompted.
mise applies its `[env]` values to tasks and `mise exec` commands. Local mise
configuration files are ignored by Git.

## Tasks

Run tasks as `mise run <name>`. `mise run` or `mise tasks ls` lists available tasks.

| Task | Behavior |
| --- | --- |
| `all` | Runs clean, tidy, fmt, vet, deadcode, arch-lint, lint, and test in order; stops on failure. |
| `clean` | Removes `.test-results`, `.cache`, `site`, `bin`, and project `.exe` files. Preserves `.git`, `.venv`, and `vendor` while scanning executables. Does not follow directory links or junctions. |
| `tidy` | Runs `go mod tidy`. |
| `fmt` | Formats Go packages with `go fmt ./...`. |
| `vet` | Runs `go vet ./...`. |
| `deadcode` | Checks `./cmd/...`; fails on findings or tool errors. |
| `arch-lint` | Checks package dependencies using `.go-arch-lint.yml`. |
| `lint` | Runs golangci-lint using `.golangci.yml`. |
| `test` | Runs Python task tests, then Go unit tests with gotestsum. |
| `test:tasks` | Runs Python task unit tests independently. |
| `run` | Starts the example application with `go run ./cmd/...`. |
| `vendor` | Runs `go mod tidy` and `go mod vendor`. |
| `deps` | Tidies modules and lists direct dependencies with available updates. |
| `release` | Validates, tags, pushes, and publishes a Go module release. |

`test` streams combined Go test output to the terminal and writes a UTF-8 log to
`.test-results/unit-<timestamp>.log`. The task fails when tests fail. `all` removes
previous logs during cleanup.

Run the Python task tests independently with:

```text
mise run test:tasks
```

Python task tests live in `.mise/tests/test_tasks.py` and use unittest discovery.
They use temporary files and mocked tools. They do not publish releases or
start the application. Directory-link coverage is skipped when the host does not
allow symlink creation.

Python file tasks have `#!/usr/bin/env python` shebangs and LF line endings.
Their executable bits are stored in Git so mise discovers and executes them on
Linux and macOS. When adding a task from Windows, use
`git add --chmod=+x -- .mise/tasks/<name>.py`. mise reads the shebang on Windows to
select the Python interpreter. Task names omit the `.py` extension.

## Dependencies

Run `mise run deps` to inspect module updates. After editing dependency versions,
run `mise run vendor` to synchronize module metadata and the vendor tree, then
review the resulting changes. Check case-only dependency path collisions when
moving a vendor tree between Windows and Linux.

## Releases

```text
mise run release 0.1.0
mise run release 0.2.0-rc.1
```

The script accepts semantic versions with an optional leading `v`. It requires
`main`, a clean working tree, authenticated GitHub CLI, and a local HEAD matching
`origin/main` after fetching. The version tag must be absent locally and on origin.

After validation, the script creates an annotated tag, pushes it to origin, and
creates a GitHub release with generated notes. Prerelease versions are marked as
prereleases. If publishing fails after the push, the error identifies the pushed
tag and the GitHub command to retry after checking for an existing release.

## Troubleshooting

If mise reports untrusted configuration, review the file it names and run
`mise trust`. If a tool is missing, run `mise install`. Use `mise exec -- <command>`
to run a tool with the project's versions without activating mise in your shell.
For failed Go tests, inspect the log path printed by `mise run test`.
