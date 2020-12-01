#!/usr/bin/env python3
"""
Solution to part 2
"""
import sys

from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, get_input, submit_output


CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

sys.path.append(str(CURRENT_DIR))

# Download input
get_input(2020, 1, INPUT_FILE_PATH)

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    data = input_fp.read()
