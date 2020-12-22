#!/usr/bin/env python3
"""
Solution to part 1
"""
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_22.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    player1, player2 = read_input(_INPUT_FILE_PATH)
    while player1 and player2:
        p1 = player1.popleft()
        p2 = player2.popleft()
        if p1 > p2:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)
    total = list(player1)[::-1] + list(player2)[::-1]
    return sum((i + 1) * n for i, n in enumerate(total))


if __name__ == "__main__":
    result = level1()
    print(result)
    print(submit_output(2020, 22, 1, result))
