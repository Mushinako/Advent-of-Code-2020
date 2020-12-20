#!/usr/bin/env python3
"""
Solution to part 2
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

mapping = str.maketrans({"B": "1", "F": "0", "R": "1", "L": "0"})

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    seat_ids = {
        int(row_stripped.translate(mapping), 2)
        for row in input_fp.readlines()
        if (row_stripped := row.strip())
    }

result = 0
for seat_id in seat_ids:
    if seat_id + 1 not in seat_ids and seat_id + 2 in seat_ids:
        result = seat_id + 1

print(result)
print(submit_output(2020, 5, 2, result))