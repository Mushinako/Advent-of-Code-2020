"""
Module: Read and parse input file

Public Functions:
    read_input: Read and parse input file
"""

from pathlib import Path


def read_input(path: Path) -> list[int]:
    """
    Read and parse the input file

    Args:
        path (Path): Input file path

    Returns:
        (list[int]): Puzzle input
    """
    with path.open("r") as fp:
        return [int(n) for n in fp.readline().strip()]
