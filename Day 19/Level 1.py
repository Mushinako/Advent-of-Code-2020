#!/usr/bin/env python3
"""
Solution to part 1
"""
import re
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> tuple[dict[str, list[str]], list[str]]:
    """
    Read and parse the input file

    Returns:
        (dict[str, list[str]]): All the rules
        (list[str])           : All the texts
    """
    rules = {}
    with _INPUT_FILE_PATH.open("r") as fp:
        while (line := fp.readline().strip()) :
            id_, pattern = line.split(": ")
            rules[id_] = ["("] + pattern.split() + [")"]

        texts = [line for l in fp if (line := l.strip())]

    return rules, texts


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    rules, texts = _read_input()
    while True:
        changed = False
        for id_, pattern_li in rules.items():
            new_pattern_li = []
            for pattern in pattern_li:
                if pattern in {"|", "(", ")"} or pattern[0] == '"':
                    new_pattern_li.append(pattern)
                else:
                    changed = True
                    new_pattern_li += rules[pattern]
            rules[id_] = new_pattern_li
        if not changed:
            break
    rule = re.compile("".join(rules["0"]).replace('"', ""))
    return sum(bool(rule.fullmatch(text)) for text in texts)


result = level1()

print(result)
print(submit_output(2020, 19, 1, result))
