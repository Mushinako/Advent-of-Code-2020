#!/usr/bin/env python3
"""
Solution to part 2
"""
from pathlib import Path
from itertools import combinations
from typing import Set

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME


def day_01_part_2(data: Set[int]) -> int:
    """Solution to Day 01 Part 2"""
    goal = 2020

    # Hidden O(n^2)
    for num1, num2 in combinations(data, 2):
        comp = goal - num1 - num2
        if comp > 0 and comp in data:
            return num1 * num2 * comp
    return 0  # Avoid linter return None complaint


# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    data = {int(line.strip()) for line in input_fp.readlines()}

result = day_01_part_2(data)

print(result)
# Submit result
print(submit_output(2020, 1, 2, result))