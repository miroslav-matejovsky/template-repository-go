#!/usr/bin/env python
#MISE description="Remove build artifacts, test results, and project executables"
"""Remove generated project artifacts while preserving dependencies and tools."""

import os
from pathlib import Path
import shutil


def clean(root: Path) -> None:
    """Clean only within root, without following directory links or junctions."""
    root = root.resolve()
    for name in (".test-results", ".cache", "site", "bin"):
        path = root / name
        if path.is_symlink() or path.is_junction():
            if path.is_symlink():
                path.unlink()
            else:
                path.rmdir()
        elif path.exists():
            if not path.resolve().is_relative_to(root):
                raise ValueError(f"cleanup path escapes repository: {path}")
            shutil.rmtree(path)

    def fail(error: OSError) -> None:
        raise error

    for directory, folders, files in os.walk(root, onerror=fail):
        folders[:] = [
            name for name in folders
            if name not in {".git", ".venv", "vendor"}
            and not (Path(directory) / name).is_symlink()
            and not (Path(directory) / name).is_junction()
        ]
        for name in files:
            if name.lower().endswith(".exe"):
                (Path(directory) / name).unlink()


if __name__ == "__main__":
    clean(Path(__file__).resolve().parent.parent)
