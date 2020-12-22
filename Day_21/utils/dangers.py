"""
Module: Danger knowledge storage

Public Classes:
    Dangers: Storage for dangerous ingredients and corresponding allergen
"""

from itertools import combinations


class Dangers:
    """
    Storage for dangerous ingredients and corresponding allergen

    Public Attributes:
        group_map (dict[frozenset[str], set[str]]):
            Mapping of a set of allergens to a set of ingredients of the same
            length. Each allergen maps to one ingredient in a 1-to-1
            relationship, but which maps to which is unknown
        individual_map (dict[str, str]):
            Mapping of an allergen to the ingredient containing it

    Public Methods:
        new_individual_maps:
            Get all new individual mappings
        mark_dangers:
            Add info about a set of dangerous ingredients and their
            corresponding allergens
    """

    def __init__(self) -> None:
        self.group_map: dict[frozenset[str], set[str]] = {}
        self._new_individual_map: dict[str, str] = {}
        self.individual_map: dict[str, str] = {}

    def new_individual_maps(self) -> tuple[set[str], set[str]]:
        """
        Get all new individual mappings

        Returns:
            (set[str]): Set of allergens
            (set[str]): Set of ingredients
        """
        if not self._new_individual_map:
            return set(), set()
        allergens: set[str] = set()
        ingredients: set[str] = set()
        for allergen, ingredient in self._new_individual_map.items():
            allergens.add(allergen)
            ingredients.add(ingredient)
            self.individual_map[allergen] = ingredient
        self._new_individual_map = {}
        return allergens, ingredients

    def mark_dangers(self, ingredients: set[str], allergens: set[str]) -> None:
        """
        Add info about a set of dangerous ingredients and their corresponding
          allergens

        The `ingredients` has to be as long as the `allergens`

        Args:
            ingredients (set[str]): Set of ingredients to be added
            allergens   (set[str]): Set of allergens to be added
        """
        if len(ingredients) != len(allergens):
            raise ValueError(
                f"# of ingredients does not equal # of allergens: "
                f"{ingredients} => {allergens}"
            )

        self._add_if_not_exists(ingredients, frozenset(allergens))

        # Clean up the clutter within the storage
        while self._clean_up():
            pass

    def _clean_up(self) -> bool:
        """
        Clean up the clutter within the storage. Called when a new danger
          entry is added

        Returns:
            (bool): Whether the `group_map` is changed
        """
        # First, move all the `group_map` entries with only 1 item to
        #   `_new_individual_map`
        for frozen_allergens, ingredients in list(self.group_map.items()):
            if len(ingredients) == 1:
                del self.group_map[frozen_allergens]
                (allergen,) = frozen_allergens
                self._new_individual_map[allergen] = ingredients.pop()

        group_map_changed = False
        for (
            (frozen_allergens_1, ingredients_1),
            (frozen_allergens_2, ingredients_2),
        ) in combinations(list(self.group_map.items()), 2):
            frozen_and_allergens = frozen_allergens_1 & frozen_allergens_2
            if not frozen_and_allergens:
                continue

            group_map_changed = True
            # Delete the orginal entries
            if frozen_allergens_1 in self.group_map:
                del self.group_map[frozen_allergens_1]
            if frozen_allergens_2 in self.group_map:
                del self.group_map[frozen_allergens_2]

            # First add intersection ingredients
            and_ingredients = ingredients_1 & ingredients_2
            assert len(frozen_and_allergens) == len(and_ingredients)
            self._add_if_not_exists(and_ingredients, frozen_and_allergens)

            # If the difference for the 1st entry is not empty, add it
            if (frozen_sub_allergens_1 := frozen_allergens_1 - frozen_and_allergens) :
                self._add_if_not_exists(
                    ingredients_1 - and_ingredients, frozen_sub_allergens_1
                )

            # If the difference for the 2nd entry is not empty, add it
            if (frozen_sub_allergens_2 := frozen_allergens_2 - frozen_and_allergens) :
                self._add_if_not_exists(
                    ingredients_2 - and_ingredients, frozen_sub_allergens_2
                )

        return group_map_changed

    def _add_if_not_exists(
        self, ingredients: set[str], frozen_allergens: frozenset[str]
    ) -> None:
        """
        If the same set of allergens is already present in storage, check if
          the ingredients are the same; else, add the entry to the storage

        Args:
            ingredients      (set[str])      : Set of ingredients to be added
            frozen_allergens (frozenset[str]): Set of allergens to be added
        """
        if frozen_allergens in self.group_map:
            assert self.group_map[frozen_allergens] == ingredients
        else:
            self.group_map[frozen_allergens] = ingredients
