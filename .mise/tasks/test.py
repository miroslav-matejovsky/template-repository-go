#!/usr/bin/env python
#MISE description="Run Python task tests and Go unit tests with saved logs"
#MISE depends=["test:tasks"]
"""Stream Go unit-test output to the terminal and a timestamped UTF-8 log."""

from datetime import datetime
from pathlib import Path
import subprocess


def run_tests(output_directory: Path) -> int:
    """Save combined output and return gotestsum's exit code unchanged."""
    output_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    log_path = output_directory / f"unit-{timestamp}.log"
    print(f"saving output to {log_path}", flush=True)
    with log_path.open("w", encoding="utf-8") as log:
        with subprocess.Popen(
            ["gotestsum", "--format", "pkgname", "./..."],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        ) as process:
            for line in process.stdout:
                print(line, end="", flush=True)
                log.write(line)
            return process.wait()


if __name__ == "__main__":
    raise SystemExit(run_tests(Path(".test-results")))
