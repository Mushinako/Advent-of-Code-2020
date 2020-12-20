#!/usr/bin/env python3
"""
Solution to part 2
"""
# pyright: reportGeneralTypeIssues=false
from functools import cache
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    jolts = [0] + [int(line.strip()) for line in input_fp]

jolts.sort()


@cache
def count_ways(jolts: tuple[int, ...]) -> int:
    if len(jolts) == 0:
        return 0
    if len(jolts) == 1:
        return 1
    if jolts[1] - jolts[0] > 3:
        return 0
    cumulative = 0
    cumulative += count_ways(jolts[1:])
    if len(jolts) == 2 or jolts[2] - jolts[0] > 3:
        return cumulative
    cumulative += count_ways(jolts[2:])
    if len(jolts) == 3 or jolts[3] - jolts[0] > 3:
        return cumulative
    return cumulative + count_ways(jolts[3:])


result = count_ways(tuple(jolts))

print(result)
print(submit_output(2020, 10, 2, result))