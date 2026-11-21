# File tasks

mise automatically discovers these executable Python scripts:

- `clean.py`: remove generated artifacts without following directory links.
- `deadcode.py`: report unreachable functions and tool errors as failures.
- `test.py`: run Go tests after `test:tasks`, save a log, and preserve the exit code.
- `release.py`: validate and publish a tagged Go module release.

Each script starts with a Python shebang and declares its task metadata with
`#MISE` comments. mise exposes names without `.py`, such as `mise run clean`.
Scripts use Python's standard library and run from the repository root.

Keep scripts executable in Git with `git add --chmod=+x -- mise-tasks/<name>.py`.
The shebang and LF line endings support direct execution on Linux and macOS;
mise uses the shebang to select Python on Windows.

Unit tests live in `scripts/test_tasks.py`. See
[development tooling](../docs/tooling.md) for commands and behavior.
