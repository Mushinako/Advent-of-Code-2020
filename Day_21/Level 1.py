#!/usr/bin/env python3
"""
Solution to part 1
"""

from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_21.utils.read_input import read_input
from Day_21.utils.ai import AllergenAI

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    foods = read_input(_INPUT_FILE_PATH)
    food_ingredients = [set(food.ingredients) for food in foods]
    allergen_ai = AllergenAI(foods)
    allergen_ai.calculate_all_new_knowledge()
    assert not allergen_ai.knowledge and not allergen_ai.dangers.group_map
    dangers = set(allergen_ai.dangers.individual_map.values())
    return sum(len(ingredients - dangers) for ingredients in food_ingredients)


if __name__ == "__main__":
    result = level1()
    print(result)
    print(submit_output(2020, 21, 1, result))
