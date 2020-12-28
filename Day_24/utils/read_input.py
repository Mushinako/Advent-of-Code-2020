"""
Module: Read and parse input file

Public Functions:
    read_input: Read and parse input file
"""

from pathlib import Path


def read_input(path: Path) -> list[list[str]]:
    """
    Read and parse the input file

    Args:
        path (Path): Input file path

    Returns:
        (list[list[str]]): Puzzle input
    """
    instructions: list[list[str]] = []
    with path.open("r") as fp:
        for l in fp:
            if (line := l.strip()) :
                steps: list[str] = []
                step = ""
                for char in line:
                    if char in {"s", "n"}:
                        step = char
                    else:
                        steps.append(step + char)
                        step = ""
                instructions.append(steps)
    return instructions
