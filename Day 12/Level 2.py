#!/usr/bin/env python3
"""
Solution to part 2
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
        direction = line[0]
        num = float(line.strip()[1:])
        moves.append((direction, num))

ship = 0.0 + 0.0j
d = 10.0 + 1.0j

for direction, num in moves:
    if direction == "N":
        d += num * (0.0 + 1.0j)
    elif direction == "S":
        d -= num * (0.0 + 1.0j)
    elif direction == "E":
        d += num * (1.0 + 0.0j)
    elif direction == "W":
        d -= num * (1.0 + 0.0j)
    elif direction == "F":
        ship += num * d
    elif direction == "L":
        d *= cmath.exp(math.radians(num) * 1.0j)
    elif direction == "R":
        d /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(direction)

result = round(abs(ship.real)) + round(abs(ship.imag))

print(result)
print(submit_output(2020, 12, 2, result))