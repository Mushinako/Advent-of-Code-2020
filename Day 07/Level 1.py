#!/usr/bin/env python3
"""
Solution to part 1
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
import re
from collections import defaultdict
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

CHILDREN_COLOR_REGEX = re.compile(r"^\d+ (?P<color>.+) bags?$")

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    map_ = defaultdict(set)
    for line in input_fp:
        line = line.strip()
        if not line:
            continue
        root_color, children = line.split(" bags contain ")
        if children == "no other bags.":
            continue
        for child in children[:-1].split(", "):
            color_match = CHILDREN_COLOR_REGEX.fullmatch(child)
            if color_match is None:
                raise ValueError(child)
            color = color_match["color"]
            map_[color].add(root_color)

stack = ["shiny gold"]
available_colors = set()

while stack:
    color = stack.pop()
    outer_colors = map_[color]
    new_colors = outer_colors - available_colors
    available_colors |= outer_colors
    stack += list(new_colors)

count = len(available_colors)

print(count)
print(submit_output(2020, 7, 1, count))