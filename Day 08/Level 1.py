#!/usr/bin/env python3
"""
Solution to part 1
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    code = []
    for line in input_fp:
        command, param = line.strip().split()
        code.append((command, int(param)))

ids = set()
acc = 0
pointer = 0

while True:
    if pointer in ids:
        break
    ids.add(pointer)
    command, param = code[pointer]
    if command == "acc":
        acc += param
        pointer += 1
    elif command == "jmp":
        pointer += param
    elif command == "nop":
        pointer += 1
    else:
        raise ValueError(f"{acc} {pointer}")

print(acc)
print(submit_output(2020, 8, 1, acc))