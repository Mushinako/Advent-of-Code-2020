#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path
from typing import Set

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME


def day_01_part_1(data: Set[int]) -> int:
    """Solution to Day 01 Part 1"""
    goal = 2020

    for num in data:
        comp = goal - num
        if comp in data:
            return num * comp
    return 0  # Avoid linter return None complaint


# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    data = {int(line.strip()) for line in input_fp.readlines()}

result = day_01_part_1(data)

print(result)
# Submit result
print(submit_output(2020, 1, 1, result))