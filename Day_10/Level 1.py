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
    jolts = [0] + [int(line.strip()) for line in input_fp]

jolts.sort()

jolt_1 = 0
jolt_3 = 1

for i, jolt in enumerate(jolts[:-1]):
    next_jolt = jolts[i + 1]
    diff = next_jolt - jolt
    if diff == 1:
        jolt_1 += 1
    elif diff == 3:
        jolt_3 += 1
    elif diff >= 4:
        break

result = jolt_1 * jolt_3

print(result)
print(submit_output(2020, 10, 1, result))