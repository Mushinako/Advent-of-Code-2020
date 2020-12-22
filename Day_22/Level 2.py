#!/usr/bin/env python3
"""
Solution to part 2
"""
from pathlib import Path
from collections import deque

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_22.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _game(player1: deque[int], player2: deque[int]) -> tuple[bool, list[int]]:
    """"""
    player1_prevs: set[frozenset[int]] = set()
    player2_prevs: set[frozenset[int]] = set()
    while True:
        if not player1:
            return False, list(player2)[::-1]
        elif not player2:
            return True, list(player1)[::-1]
        if (p1f := frozenset(player1)) in player1_prevs or (
            p2f := frozenset(player2)
        ) in player2_prevs:
            return True, list(player1)[::-1]
        player1_prevs.add(p1f)
        player2_prevs.add(p2f)
        p1 = player1.popleft()
        p2 = player2.popleft()
        if p1 <= len(player1) and p2 <= len(player2):
            winner, _ = _game(deque(list(player1)[:p1]), deque(list(player2)[:p2]))
            if winner:
                player1.append(p1)
                player1.append(p2)
            else:
                player2.append(p2)
                player2.append(p1)
        else:
            if p1 > p2:
                player1.append(p1)
                player1.append(p2)
            else:
                player2.append(p2)
                player2.append(p1)


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    player1, player2 = read_input(_INPUT_FILE_PATH)
    _, winning_deck = _game(player1, player2)
    return sum((i + 1) * n for i, n in enumerate(winning_deck))


if __name__ == "__main__":
    result = level2()
    print(result)
    print(submit_output(2020, 22, 2, result))
