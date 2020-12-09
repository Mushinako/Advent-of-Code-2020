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
    nums = [int(line.strip()) for line in input_fp]

target = 373803594


def main() -> int:
    for i, num_start in enumerate(nums):
        sum_ = num_start
        for j, num in enumerate(nums[i + 1 :]):
            sum_ += num
            if sum_ > target:
                break
            if sum_ == target:
                arr = nums[i : i + j + 2]
                return min(arr) + max(arr)
    return 0  # Make linter happy


sum_ = main()

print(sum_)
print(submit_output(2020, 9, 2, sum_))