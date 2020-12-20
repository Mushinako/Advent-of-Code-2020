#!/usr/bin/env python3
"""
Solution to part 2
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
        value = int(value)
        binary = bin(index)[2:].zfill(36)
        new_binary = ""
        floatings = []
        for i in range(36):
            if mask[i] == "0":
                new_binary += binary[i]
            elif mask[i] == "1":
                new_binary += "1"
            else:
                new_binary += "0"
                floatings.append(35 - i)
        base_num = int(new_binary, 2)
        for i in range(2 ** len(floatings)):
            new_num = base_num
            for j, power in enumerate(floatings):
                i, rem = divmod(i, 2)
                if rem:
                    new_num += 2 ** power
            memory[new_num] = value

result = sum(memory.values())

print(result)
print(submit_output(2020, 14, 2, result))