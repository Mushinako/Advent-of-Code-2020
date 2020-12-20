#!/usr/bin/env python3
"""
Solution to part 1
"""
import math
import cmath
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    moves = []
    for line in input_fp:
        action = line[0]
        num = float(line.strip()[1:])
        moves.append((action, num))

position = 0.0 + 0.0j
direction = 1.0 + 0.0j

for action, num in moves:
    if action == "N":
        position += num * (0.0 + 1.0j)
    elif action == "S":
        position -= num * (0.0 + 1.0j)
    elif action == "E":
        position += num * (1.0 + 0.0j)
    elif action == "W":
        position -= num * (1.0 + 0.0j)
    elif action == "F":
        position += num * direction
    elif action == "L":
        direction *= cmath.exp(math.radians(num) * 1.0j)
    elif action == "R":
        direction /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(action)

result = round(abs(position.real)) + round(abs(position.imag))

print(result)
print(submit_output(2020, 12, 1, result))