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
    instructions = [line.split(" = ") for line in input_fp.readlines() if line]

memory: dict[int, int] = {}

mask = ""

for action, value in instructions:
    if action == "mask":
        mask = value
    else:
        index = int(action[4:-1])
        binary = bin(int(value))[2:].zfill(36)
        new_binary = ""
        for i in range(36):
            if mask[i] == "X":
                new_binary += binary[i]
            else:
                new_binary += mask[i]
        memory[index] = int(new_binary, 2)

result = sum(memory.values())

print(result)
print(submit_output(2020, 14, 1, result))