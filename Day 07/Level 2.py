#!/usr/bin/env python3
"""
Solution to part 2
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

CHILDREN_COLOR_REGEX = re.compile(r"(?P<count>^\d+) (?P<color>.+) bags?$")

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    map_: defaultdict[str, dict[str, int]] = defaultdict(dict)
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
            count = int(color_match["count"])
            color = color_match["color"]
            map_[root_color][color] = count

stack: defaultdict[str, int] = defaultdict(lambda: 0)
stack["shiny gold"] = 1
total_count = 0

while stack:
    parent_color = next(iter(stack))
    parent_count = stack[parent_color]
    del stack[parent_color]
    rules = map_[parent_color]
    for child_color, child_count in rules.items():
        mul_child_count = parent_count * child_count
        total_count += mul_child_count
        stack[child_color] += mul_child_count

print(total_count)
print(submit_output(2020, 7, 2, total_count))