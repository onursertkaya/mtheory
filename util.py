"""Miscellaneous utilities."""
import shlex
from pathlib import Path
from subprocess import run
from typing import List


def cumulative_sum(sequence: List[int]) -> List[int]:
    """Naive implementation of cumulative sum of a sequence."""
    summed = []
    for idx in range(1, len(sequence) + 1):
        summed.append(sum(sequence[:idx]))
    return summed


def check():
    """Run python formatting and code quality jobs."""
    run(shlex.split("python3 -m black . --line-length 100"), check=True)
    run(shlex.split("python3 -m isort . --profile black"), check=True)

    repo_root = run(
        shlex.split("git rev-parse --show-toplevel"),
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip("\n ")

    py_files = [str(p) for p in Path(repo_root).rglob("*.py")]
    # To be able to run all jobs, ignore check=True.
    # pylint: disable=subprocess-run-check
    run(shlex.split(f"python3 -m pylint {' '.join(py_files)}"))
    run(shlex.split(f"python3 -m mypy {' '.join(py_files)}"))
