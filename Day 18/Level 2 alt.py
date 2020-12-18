#!/usr/bin/env python3
"""
Solution to part 2
"""
# pyright: reportMissingTypeStubs=false
from pathlib import Path

from forbiddenfruit import curse

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> list[str]:
    """
    Read and parse the input file

    Returns:
        (list[list[bool]]): Puzzle input
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        lines = [line for l in fp if (line := l.strip())]

    return lines


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    lines = _read_input()
    return sum(eval(line.replace("+", "**")) for line in lines)


curse(int, "__pow__", lambda self, other: self + other)  # type: ignore

result = level2()

print(result)
print(submit_output(2020, 18, 2, result))
