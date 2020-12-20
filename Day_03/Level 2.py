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
    map_ = [cleaned_row for row in input_fp.readlines() if (cleaned_row := row.strip())]

moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
map_width = len(map_[0])

result = 1

for right, down in moves:
    spaces = [map_[i * down][i * right % map_width] for i in range(len(map_) // down)]
    count = spaces.count("#")
    result *= count

print(result)
print(submit_output(2020, 3, 2, result))