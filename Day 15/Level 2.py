#!/usr/bin/env python3
"""
Solution to part 2
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    nums = [int(num) for num in input_fp.readline().strip().split(",")]

nums_dict = {num: i + 1 for i, num in enumerate(nums[:-1])}
consideration = nums[-1]

for i in range(len(nums), 30_000_000):
    if consideration in nums_dict:
        new_last_num = i - nums_dict[consideration]
    else:
        new_last_num = 0
    nums_dict[consideration] = i
    consideration = new_last_num

result = consideration

print(result)
print(submit_output(2020, 15, 2, result))