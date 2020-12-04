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
    people = input_fp.read().replace("\n", " ").split("  ")

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

count = 0

for person in people:
    keys = {entry.split(":")[0] for entry in person.split()}
    if keys >= REQUIRED:
        count += 1

print(count)
print(submit_output(2020, 4, 1, count))