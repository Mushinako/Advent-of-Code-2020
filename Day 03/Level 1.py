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
    map_ = [cleaned_row for row in input_fp.readlines() if (cleaned_row := row.strip())]

map_width = len(map_[0])
right = 3
spaces = [map_[i][i * right % map_width] for i in range(len(map_))]
result = spaces.count("#")

print(result)
print(submit_output(2020, 3, 1, result))