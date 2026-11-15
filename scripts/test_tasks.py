"""Test task behavior without running Go tools or publishing releases."""

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

# Import the task files without executing their command-line entry points.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mise-tasks"))

import clean
import deadcode
import release
import test as go_test


class CleanTests(unittest.TestCase):
    def test_removes_artifacts_and_preserves_sources_and_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            removed = [
                "bin/app", ".cache/item", ".test-results/unit.log",
                "site/index.html", "cmd/app.exe",
            ]
            kept = ["cmd/main.go", ".venv/tool.exe", "vendor/tool.exe", ".git/tool.exe"]
            for name in removed + kept:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("keep or remove", encoding="utf-8")
            clean.clean(root)
            for name in removed:
                self.assertFalse((root / name).exists(), name)
            for name in kept:
                self.assertTrue((root / name).exists(), name)
            clean.clean(root)  # Repeated cleanup is safe.

    def test_does_not_follow_artifact_directory_links(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            target = Path(outside)
            (target / "keep.exe").touch()
            try:
                (root / "bin").symlink_to(target, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlinks unavailable: {error}")
            clean.clean(root)
            self.assertTrue((target / "keep.exe").exists())


class DeadcodeTests(unittest.TestCase):
    @patch("deadcode.subprocess.run")
    def test_findings_and_tool_errors_fail(self, run):
        cases = [
            (0, "", 0),
            (0, "main.go:3: unreachable func: unused\n", 1),
            (2, "build failed\n", 2),
        ]
        for code, output, expected in cases:
            with self.subTest(code=code, output=output):
                run.return_value = subprocess.CompletedProcess([], code, output)
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    self.assertEqual(deadcode.check(), expected)
                if output:
                    self.assertIn(output.strip(), stdout.getvalue())


class TestLogTests(unittest.TestCase):
    @patch("test.subprocess.Popen")
    def test_logs_combined_output_and_returns_test_exit_code(self, popen):
        process = Mock()
        process.stdout = io.StringIO("passing test\nfailing test\n")
        process.wait.return_value = 7
        popen.return_value.__enter__.return_value = process
        with tempfile.TemporaryDirectory() as directory:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(go_test.run_tests(Path(directory)), 7)
            logs = list(Path(directory).glob("unit-*.log"))
            self.assertEqual(len(logs), 1)
            self.assertEqual(
                logs[0].read_text(encoding="utf-8"),
                "passing test\nfailing test\n",
            )
            self.assertIn("failing test", stdout.getvalue())


class ReleaseTests(unittest.TestCase):
    def test_validates_semver_before_running_commands(self):
        with patch("release.subprocess.run") as run:
            for version in ["", "1.2", "01.2.3", "1.2.3-01", "1.2.3-a..b"]:
                with self.subTest(version=version), self.assertRaises(ValueError):
                    release.release(version)
            run.assert_not_called()

    def release_commands(self, version, overrides=None):
        responses = {
            ("git", "rev-parse", "--abbrev-ref", "HEAD"): "main",
            ("git", "status", "--porcelain"): "",
            ("git", "remote", "get-url", "--push", "origin"):
                "https://github.com/example/project.git",
            ("git", "rev-parse", "HEAD"): "abc123",
            ("git", "rev-parse", "origin/main"): "abc123",
        }
        responses.update(overrides or {})
        self.commands = []

        def run(args, **kwargs):
            self.commands.append(args)
            value = responses.get(tuple(args), "")
            if isinstance(value, Exception):
                raise value
            return subprocess.CompletedProcess(args, 0, value)

        with patch("release.subprocess.run", side_effect=run), contextlib.redirect_stdout(io.StringIO()):
            release.release(version)
        return self.commands

    def test_release_normalizes_version_and_marks_prereleases(self):
        for version, prerelease in [("1.2.3", False), ("v1.2.3-rc.1+build.2", True)]:
            with self.subTest(version=version):
                commands = self.release_commands(version)
                tag = version if version.startswith("v") else f"v{version}"
                self.assertIn(
                    ["git", "tag", "-a", tag, "-m", f"Release {tag}"], commands,
                )
                self.assertIn(["git", "push", "origin", tag, "--quiet"], commands)
                self.assertEqual("--prerelease" in commands[-1], prerelease)

    def test_preconditions_prevent_tagging(self):
        cases = [
            {("git", "rev-parse", "--abbrev-ref", "HEAD"): "feature"},
            {("git", "status", "--porcelain"): " M README.md"},
            {("gh", "auth", "status"): FileNotFoundError("gh")},
            {("gh", "auth", "status"): subprocess.CalledProcessError(1, "gh")},
            {("git", "rev-parse", "origin/main"): "other"},
            {("git", "tag", "--list", "v1.2.3"): "v1.2.3"},
            {("git", "ls-remote", "--tags", "origin", "refs/tags/v1.2.3"): "abc refs/tags/v1.2.3"},
        ]
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                    self.release_commands("1.2.3", overrides)
                for command in self.commands:
                    self.assertNotEqual(command[:3], ["git", "tag", "-a"])
                    self.assertNotEqual(command[:2], ["git", "push"])
                    self.assertNotEqual(command[:3], ["gh", "release", "create"])

    def test_failed_push_prevents_publishing(self):
        command = ("git", "push", "origin", "v1.2.3", "--quiet")
        with self.assertRaises(subprocess.CalledProcessError):
            self.release_commands(
                "1.2.3", {command: subprocess.CalledProcessError(1, command)},
            )
        self.assertFalse(any(args[:3] == ["gh", "release", "create"] for args in self.commands))

    def test_failed_publish_reports_already_pushed_tag(self):
        command = (
            "gh", "release", "create", "v1.2.3", "--repo",
            "https://github.com/example/project.git", "--verify-tag",
            "--title", "v1.2.3", "--generate-notes",
        )
        with self.assertRaisesRegex(RuntimeError, "tag v1.2.3 was pushed"):
            self.release_commands("1.2.3", {command: subprocess.CalledProcessError(1, command)})


if __name__ == "__main__":
    unittest.main()
