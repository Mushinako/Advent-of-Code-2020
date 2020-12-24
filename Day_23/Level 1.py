#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_23.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def level1() -> str:
    """
    Level 1 solution

    Returns:
        (str): Solution to the problem
    """
    cups: list[int] = read_input(_INPUT_FILE_PATH)
    max_ = max(cups)
    for _ in range(100):
        # Current element
        current = cups[0]
        # Elements not touched this loop
        left = cups[4:]
        left_set = set(left)
        # Find the next smallest value in the numbers left; wrap around to
        #   `max_` if the value decreases to 0
        while True:
            current -= 1
            if not current:
                current = max_
            if current in left_set:
                break
        # Add the 3 cups after the destination value, and then move the current
        #   value to the end of the list
        dest_index = cups.index(current) + 1
        cups = cups[4:dest_index] + cups[1:4] + cups[dest_index:] + cups[:1]
    index_1 = cups.index(1)
    return "".join(str(n) for n in (cups[index_1 + 1 :] + cups[:index_1]))


if __name__ == "__main__":
    result = level1()
    print(result)
    print(submit_output(2020, 23, 1, result))
