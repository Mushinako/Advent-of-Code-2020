#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

mapping = str.maketrans({"B": "1", "F": "0", "R": "1", "L": "0"})

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    result = max(
        int(row_stripped.translate(mapping), 2)
        for row in input_fp.readlines()
        if (row_stripped := row.strip())
    )

print(result)
print(submit_output(2020, 5, 1, result))