#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    nums = [int(num) for num in input_fp.readline().strip().split(",")]

while len(nums) < 2020:
    consideration = nums[-1]
    if nums.count(consideration) == 1:
        nums.append(0)
    else:
        gap = nums[::-1][1:].index(consideration) + 1
        nums.append(gap)

result = nums[-1]

print(result)
print(submit_output(2020, 15, 1, result))