#!/usr/bin/env python3
"""
Solution to part 2
"""
# pyright: reportGeneralTypeIssues=false
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    map_ = [list(line.strip()) for line in input_fp]

height = len(map_)
width = len(map_[0])
directions = [(r, c) for r in range(-1, 2) for c in range(-1, 2) if r or c]


def get_neighbor_occupied(map_: list[list[str]], coord: tuple[int, int]) -> int:
    row, col = coord
    count = 0
    for dr, dc in directions:
        r = row
        c = col
        while 0 <= (r := r + dr) < height and 0 <= (c := c + dc) < width:
            if map_[r][c] == ".":
                continue
            if map_[r][c] == "#":
                count += 1
            break
    return count


while True:
    new_map = [row[:] for row in map_]
    for r in range(height):
        for c in range(width):
            if map_[r][c] == ".":
                continue
            elif map_[r][c] == "L":
                if get_neighbor_occupied(map_, (r, c)) == 0:
                    new_map[r][c] = "#"
            elif map_[r][c] == "#":
                if get_neighbor_occupied(map_, (r, c)) >= 5:
                    new_map[r][c] = "L"
            else:
                raise ValueError(f"{(r, c)} {new_map[r][c]}")
    if new_map == map_:
        break
    map_ = new_map

result = sum(row.count("#") for row in map_)

print(result)
print(submit_output(2020, 11, 2, result))