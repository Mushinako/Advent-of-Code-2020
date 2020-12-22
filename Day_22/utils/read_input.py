"""
Module: Read and parse input file

Public Functions:
    read_input: Read and parse input file
"""

from pathlib import Path
from collections import deque


def read_input(path: Path) -> tuple[deque[int], deque[int]]:
    """
    Read and parse the input file

    Args:
        path (Path): Input file path

    Returns:
        (tuple[deque[int], deque[int]]): Puzzle input
    """
    with path.open("r") as fp:
        player1, player2 = fp.read().split("\n\n")

    return (
        deque(int(n) for n in player1.splitlines()[1:]),
        deque(int(n) for n in player2.splitlines()[1:]),
    )
