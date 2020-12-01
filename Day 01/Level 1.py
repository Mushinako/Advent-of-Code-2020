#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

DATA_FILENAME = "input.txt"


CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# sys.path.append(str(CURRENT_DIR))

# Download input
# get_input(2020, 1, INPUT_FILE_PATH)

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    data = {int(line.strip()) for line in input_fp.readlines()}

GOAL = 2020

for num in data:
    comp = GOAL - num
    if comp in data:
        print(num * comp)
        break
