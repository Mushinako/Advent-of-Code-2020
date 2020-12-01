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
    data = {int(line.strip()) for line in input_fp.readlines()}

GOAL = 2020

result = 0

for num in data:
    comp = GOAL - num
    if comp in data:
        result = num * comp
        break

print(result)
print(submit_output(2020, 2, 1, result))