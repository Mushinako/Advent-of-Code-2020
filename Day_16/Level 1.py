#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> tuple[set[int], list[int]]:
    """
    Read and parse the input file

    Returns:
        (set[int]) : Set of all numbers that are valid in at least one rule
        (list[int]): List of all numbers present in nearby tickets
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        # Rules
        # This is quite space-inefficient but meh
        rule_nums = set()
        while (line := fp.readline().strip()) :
            _, ranges_str = line.split(": ")
            for r in ranges_str.split(" or "):
                start, end = r.split("-")
                rule_nums |= set(range(int(start), int(end) + 1))
        # Your ticket, ignored
        for _ in range(4):
            fp.readline()
        # Nearby tickets
        nearby_nums = [int(n) for line in fp for n in line.strip().split(",")]
    return rule_nums, nearby_nums


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    rule_nums, nearby_nums = _read_input()
    return sum(n for n in nearby_nums if n not in rule_nums)


result = level1()

print(result)
print(submit_output(2020, 16, 1, result))