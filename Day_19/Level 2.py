#!/usr/bin/env python3
"""
Solution to part 2
"""
from pathlib import Path

from lark import Lark, LarkError

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> tuple[str, list[str]]:
    """
    Read and parse the input file

    Returns:
        (str)      : All the rules, newline-separated
        (list[str]): All the texts
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        rules, messages = fp.read().split("\n\n")

    # 8 special case
    rules = rules.replace("8: 42", "8: 42 | 42 8")

    # 11 special case
    rules = rules.replace("11: 42 31", "11: 42 31 | 42 11 31")

    # Convert all the numbers to letters
    rules = rules.translate(str.maketrans("123456789", "cdefghijk"))
    rules = rules.replace("0", "start")

    texts = [line.strip() for l in messages.splitlines() if (line := l.strip())]

    return rules, texts


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    rules, texts = _read_input()
    parser = Lark(rules)

    result = 0
    for text in texts:
        try:
            parser.parse(text)
        except LarkError:
            # Not a solution
            continue
        else:
            result += 1
    return result


result = level2()

print(result)
print(submit_output(2020, 19, 2, result))