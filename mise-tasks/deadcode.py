#!/usr/bin/env python
#MISE description="Fail on unreachable functions in cmd entry points"
"""Fail on dead-code findings and preserve tool or build diagnostics."""

import subprocess


def check() -> int:
    """Return a failure for findings or a failed deadcode invocation."""
    result = subprocess.run(
        ["deadcode", "./cmd/..."], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False,
    )
    if result.stdout.strip():
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.returncode:
        return result.returncode
    if result.stdout.strip():
        return 1
    print("deadcode: no issues found")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
