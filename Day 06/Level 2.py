#!/usr/bin/env python3
"""
Solution to part 2
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    groups = [group for g in input_fp.read().split("\n\n") if (group := g.strip())]

count = 0
for group in groups:
    people = group.split()
    responses = set.intersection(*[set(person) for person in people])
    count += len(responses)

print(count)
print(submit_output(2020, 6, 2, count))