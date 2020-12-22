#!/usr/bin/env python3
"""
Solution to part 2
"""

from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_21.utils.read_input import read_input
from Day_21.utils.ai import AllergenAI

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def level2() -> str:
    """
    Level 2 solution

    Returns:
        (str): Solution to the problem
    """
    foods = read_input(_INPUT_FILE_PATH)
    allergen_ai = AllergenAI(foods)
    allergen_ai.calculate_all_new_knowledge()
    assert not allergen_ai.knowledge and not allergen_ai.dangers.group_map
    return ",".join(
        element[1] for element in sorted(allergen_ai.dangers.individual_map.items())
    )


if __name__ == "__main__":
    result = level2()
    print(result)
    print(submit_output(2020, 21, 2, result))
