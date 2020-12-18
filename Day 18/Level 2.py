#!/usr/bin/env python3
"""
Solution to part 2
"""
import re
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> list[str]:
    """
    Read and parse the input file

    Returns:
        (list[list[bool]]): Puzzle input
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        lines = [line for l in fp if (line := l.strip())]

    return lines


def _solve_simple(formula: str) -> int:
    """
    Solve a "simple" formula; i.e., a formula without parentheses

    Args:
        formula (str): The formula section without parentheses

    Returns:
        (int): Result for this formula section
    """
    addition = re.compile(r"(\d+) \+ (\d+)")
    while "+" in formula:
        formula = addition.sub(
            lambda match: str(int(match[1]) + int(match[2])), formula, count=1
        )
    result = 1
    for token in formula.split():
        if token.isdigit():
            result *= int(token)
        elif token == "*":
            continue
        else:
            raise ValueError(token)
    return result


def _solve_line(line: str) -> int:
    """
    Solve a line of formula

    Args:
        line (str): A line of formula

    Returns:
        (int): Result for this line
    """
    paren_re = re.compile(r"\(([^()]+)\)")
    while "(" in line:
        line = paren_re.sub(lambda match: str(_solve_simple(match[1])), line, count=1)
    return _solve_simple(line)


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    lines = _read_input()
    return sum(_solve_line(line) for line in lines)


result = level2()

print(result)
print(submit_output(2020, 18, 2, result))
