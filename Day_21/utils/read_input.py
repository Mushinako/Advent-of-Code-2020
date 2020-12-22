"""
Module: Read and parse input file

Public Functions:
    read_input: Read and parse input file
"""

from pathlib import Path

from .sentence import Sentence


def read_input(path: Path) -> list[Sentence]:
    """
    Read and parse input file

    Args:
        path (Path): Input file path

    Returns:
        (list[Sentence]): Parsed input file
    """
    with path.open("r") as fp:
        return [Sentence.from_input_line(line) for l in fp if (line := l.strip())]
