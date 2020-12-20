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
    ts = int(input_fp.readline().strip())
    buses = [int(num) for num in input_fp.readline().strip().split(",") if num != "x"]

schedules = [(b - ts % b, b) for b in buses]

min_ = min(schedules)
result = min_[0] * min_[1]

print(result)
print(submit_output(2020, 13, 1, result))