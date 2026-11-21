#!/usr/bin/env python
#MISE description="Tag, push, and publish a release from main: mise run release 0.1.0"
#MISE raw_args=true
"""Validate main, push an annotated module tag, and publish a GitHub release."""

import argparse
import re
import subprocess


def release(version: str) -> None:
    """Publish a semantic version only from a clean main matching origin/main."""
    version = version.strip()
    if not version.startswith("v"):
        version = f"v{version}"
    number = r"(?:0|[1-9][0-9]*)"
    identifier = rf"(?:{number}|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    semver = (
        rf"v{number}\.{number}\.{number}"
        rf"(?:-{identifier}(?:\.{identifier})*)?"
        r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    )
    if not re.fullmatch(semver, version):
        raise ValueError(f"invalid version '{version}', expected semver like 0.1.0 or v0.1.0")

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], check=True, stdout=subprocess.PIPE, text=True,
        ).stdout.strip()

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        raise ValueError(f"must be on main, current branch is '{branch}'")
    status = git("status", "--porcelain")
    if status:
        raise ValueError(f"working tree has uncommitted changes:\n{status}")
    try:
        subprocess.run(["gh", "auth", "status"], check=True)
    except FileNotFoundError as error:
        raise ValueError("GitHub CLI (gh) is required; install it and run 'gh auth login'") from error
    origin = git("remote", "get-url", "--push", "origin")
    git("fetch", "origin", "main", "--tags", "--quiet")
    local = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/main")
    if local != remote:
        raise ValueError("main differs from origin/main, push or pull first")
    if git("tag", "--list", version):
        raise ValueError(f"tag {version} already exists locally")
    if git("ls-remote", "--tags", "origin", f"refs/tags/{version}"):
        raise ValueError(f"tag {version} already exists on origin")

    git("tag", "-a", version, "-m", f"Release {version}")
    git("push", "origin", version, "--quiet")
    command = [
        "gh", "release", "create", version, "--repo", origin,
        "--verify-tag", "--title", version, "--generate-notes",
    ]
    if "-" in version.split("+", 1)[0]:
        command.append("--prerelease")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"GitHub release creation failed; tag {version} was pushed. "
            f"Check GitHub for an existing release before retrying: {' '.join(command)}"
        ) from error
    print(f"released {version} at {local}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="semantic version, with an optional leading v")
    arguments = parser.parse_args()
    try:
        release(arguments.version)
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"release: {error}\n")
