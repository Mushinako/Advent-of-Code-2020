"""
Module: Knowledge sentence

Public Classes:
    Sentence: A knowledge sentence
"""

from __future__ import annotations


class Sentence:
    """
    A knowledge sentence

    Args:
        ingredients (set[str]): Set of all ingredients
        allergens   (set[str]): Set of all allergens

    Public Attributes:
        ingredients (set[str]): Set of all ingredients
        allergens   (set[str]): Set of all allergens

    Public Read-only Properties:
        known_dangers (set[str]):
            Known dangerous ingredients that can be derived from this sentence

    Public Methods:
        mark_dangers: Mark some ingredients as dangerous

    Public Class Methods:
        from_input_line: Create instance from a line of input string

    """

    def __init__(self, ingredients: set[str], allergens: set[str]) -> None:
        self.ingredients = ingredients
        self.allergens = allergens

    def __eq__(self, other: Sentence) -> bool:
        return (
            self.ingredients == other.ingredients and self.allergens == other.allergens
        )

    def __repr__(self) -> str:
        return f"Sentence({self.ingredients} => {self.allergens})"

    @property
    def known_dangers(self) -> set[str]:
        """
        Property: known_dangers (set[str])

        Known dangerous ingredients that can be derived from this sentence

        If the length of `self.ingredients` and that of `self.allergens` are
          the same, then all the ingredients are dangerous. Otherwise, nothing
          can be inferred
        """
        if len(self.ingredients) - len(self.allergens):
            return set()
        else:
            return self.ingredients

    def mark_dangers(self, ingredients: set[str], allergens: set[str]) -> None:
        """
        Mark some ingredients as dangerous

        Effectively, remove all the ingredients and allergens listed from self

        Args:
            ingredients (set[str]): Set of known dangerous ingredients
            allergens   (set[str]): Set of knwon allergens associated
        """
        self.ingredients -= ingredients
        self.allergens -= allergens

    @classmethod
    def from_input_line(cls, line: str) -> Sentence:
        """
        Create instance from a line of input string

        Args:
            line (str): A line of input string

        Returns:
            (Sentence): Constructed instance
        """
        ingredients, allergens = line[:-1].split(" (contains ")
        ingredient_set = set(ingredients.split())
        allergen_set = set(allergens.split(", "))
        return cls(ingredient_set, allergen_set)