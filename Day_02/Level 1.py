#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input. This time I'll do the processing while reading
count = 0
with INPUT_FILE_PATH.open("r") as input_fp:
    count = 0
    for line in input_fp:
        if not (line := line.strip()):
            break
        counts, letter, password = line.split()
        lower, upper = [int(n) for n in counts.split("-")]
        letter = letter[0]
        if lower <= password.count(letter) <= upper:
            count += 1


print(count)
print(submit_output(2020, 2, 1, count))