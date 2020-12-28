#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path
from collections import defaultdict

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_24.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    instructions = read_input(_INPUT_FILE_PATH)
    tiles_changed: defaultdict[complex, bool] = defaultdict(lambda: False)
    for instruction in instructions:
        coord = 0 + 0j
        for step in instruction:
            if step == "e":
                coord += 1
            elif step == "w":
                coord -= 1
            elif step == "nw":
                coord += 1j
            elif step == "se":
                coord -= 1j
            elif step == "ne":
                coord += 1 + 1j
            elif step == "sw":
                coord -= 1 + 1j
            else:
                raise ValueError(f"Unknown step: {step}")
        tiles_changed[coord] ^= True
    return sum(tiles_changed.values())


if __name__ == "__main__":
    result = level1()
    print(result)
    print(submit_output(2020, 24, 1, result))
