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
    code = []
    for line in input_fp:
        command, param = line.strip().split()
        code.append((command, int(param)))


def main(code: list[tuple[str, int]]) -> int:
    for i in range(len(code)):
        if code[i][0] == "jmp":
            replacement = "nop"
        elif code[i][0] == "nop":
            replacement = "jmp"
        else:
            continue

        new_code = [list(a) for a in code]
        new_code[i][0] = replacement

        ids = set()
        acc: int = 0
        pointer: int = 0

        while True:
            if pointer >= len(new_code):
                return acc
            if pointer in ids:
                break
            ids.add(pointer)
            command, param = new_code[pointer]
            if command == "acc":
                acc += param
                pointer += 1
            elif command == "jmp":
                pointer += param
            elif command == "nop":
                pointer += 1
            else:
                raise ValueError(f"{acc} {pointer}")
    return 0  # Make linter happy


acc = main(code)

print(acc)
print(submit_output(2020, 8, 2, acc))