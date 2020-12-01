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
    data = {int(line.strip()) for line in input_fp.readlines()}

GOAL = 2020

data_tuple = tuple(data)

result = 0

for i, num1 in enumerate(data_tuple[:-2]):
    for num2 in data_tuple[i + 1 :]:
        comp = GOAL - num1 - num2
        if comp > 0 and comp in data:
            result = num1 * num2 * comp
            break

print(result)
print(submit_output(2020, 2, 2, result))