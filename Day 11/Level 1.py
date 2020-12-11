#!/usr/bin/env python3
"""
Solution to part 1
"""
# pyright: reportGeneralTypeIssues=false
from itertools import product
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    map_ = [list(line.strip()) for line in input_fp]

height = len(map_)
width = len(map_[0])


def get_neighbor_occupied(map_: list[list[str]], coord: tuple[int, int]) -> int:
    row, col = coord
    count = sum(
        map_[r][c] == "#"
        for r, c in product(range(row - 1, row + 2), range(col - 1, col + 2))
        if 0 <= r < height and 0 <= c < width and (r != row or c != col)
    )
    return count


while True:
    new_map = [list(row) for row in map_]
    for r, c in product(range(height), range(width)):
        if map_[r][c] == ".":
            continue
        if map_[r][c] == "L":
            if get_neighbor_occupied(map_, (r, c)) == 0:
                new_map[r][c] = "#"
        else:
            if get_neighbor_occupied(map_, (r, c)) >= 4:
                new_map[r][c] = "L"
    if new_map == map_:
        break
    map_ = new_map

result = sum(row.count("#") for row in map_)

print(result)
print(submit_output(2020, 11, 1, result))