"""
Module: AI solver

Public Classes:
    AllergenAI: An AI to solve the allergen issue
"""

from itertools import combinations

from .sentence import Sentence
from .dangers import Dangers


class AllergenAI:
    """
    Allergen AI solver

    Args:
        base_knowledge (list[Sentence]): Initial knowledges

    Public Attributes:
        knowledge (list[Sentence]): All knowledge the AI possesses
        dangers   (Dangers)       : All the known danger information

    Public Methods:
        calculate_all_new_knowledge:
            Keep cleaning up and calculating new knowledge until no new
            knowledge can be inferred
        clean_up_knowledge:
            Clean up the knowledge base, removing duplicates and check for new
            information of known dangers and remove them from the knowledge base
        calculate_new_knowledge:
            Try to get new knowledge from current knowledge base
    """

    def __init__(self, base_knowledge: list[Sentence]) -> None:
        self.knowledge = base_knowledge
        self.dangers = Dangers()

    def calculate_all_new_knowledge(self) -> None:
        """
        Keep cleaning up and calculating new knowledge until no new knowledge
          can be inferred
        """
        while True:
            # `clean_up_knowledge` returns whether any modification to any
            #   sentence has taken place. Keep cleaning up until no modification
            while self.clean_up_knowledge():
                pass
            # `calculate_new_knowledge` returns whether any new knowledge is
            #   added. Keep calculating and cleaning until no new knoledge
            if not self.calculate_new_knowledge():
                break

    def clean_up_knowledge(self) -> bool:
        """
        Clean up the knowledge base, removing duplicates and check for new
          information of known dangers and remove them from the knowledge base
        """
        sentences_changed = False

        # Shallow copy the knowledge base to iterate through
        for sentence in list(self.knowledge):
            # Ignore removed sentences
            if sentence not in self.knowledge:
                continue

            # Get rid of sentences with no allergens. Not useful
            if not sentence.allergens:
                self.knowledge.remove(sentence)
                continue

            # Check if dangers can be inferred from this sentence
            if (dangers := sentence.known_dangers) :
                sentences_changed = True
                self._mark_dangers(dangers, sentence.allergens)

        return sentences_changed

    def calculate_new_knowledge(self) -> bool:
        """
        Try to get new knowledge from current knowledge base
        """
        knowledge_changed = False

        for this_sentence, other_sentence in combinations(list(self.knowledge), 2):
            # No need to do the ones not present in knowledge base
            if (
                this_sentence not in self.knowledge
                or other_sentence not in self.knowledge
            ):
                continue

            this_allergens = this_sentence.allergens
            this_ingredients = this_sentence.ingredients
            other_allergens = other_sentence.allergens
            other_ingredients = other_sentence.ingredients
            # For sentences with the same ingredients, the allergen can be
            #   present in either, because sometimes allergens may not be marked
            if this_ingredients == other_ingredients:
                this_allergens |= other_allergens
                self.knowledge.remove(other_sentence)
                continue

            # Try to find new sentences
            # If allergen is subset, update the smaller one directly, as the
            #   same ingredient must be present in the larger set
            if this_allergens < other_allergens:
                this_ingredients &= other_ingredients
                continue
            if this_allergens > other_allergens:
                other_ingredients &= this_ingredients
                continue

            # Same allergen. Ingredient must in both. Update one and remove the
            #   other
            if this_allergens == other_allergens:
                this_allergens &= other_allergens
                self.knowledge.remove(other_sentence)
                continue

            # Take intersection
            new_allergens = this_allergens & other_allergens
            # No overlap, no new info can be inferred
            if not new_allergens:
                continue
            new_ingredients = this_ingredients & other_ingredients

            # Sanity check
            if len(new_ingredients) < len(new_allergens):
                raise ValueError(
                    f"# of ingredients smaller than # of allergens: "
                    f"{new_ingredients} => {new_allergens}"
                )

            # Check if same knowledge already covered by another sentence
            for test_sentence in self.knowledge:
                # Allergens covered. Update the ingredients as the ones present
                #   in both
                if test_sentence.allergens == new_allergens:
                    test_sentence.ingredients &= new_ingredients
                    break

                # Ingredients covered. Update the allergens as the ones present
                #   in either
                if test_sentence.ingredients == new_ingredients:
                    test_sentence.allergens |= new_allergens
                    break

            # No match found. Add sentence
            else:
                knowledge_changed = True
                self.knowledge.append(Sentence(new_ingredients, new_allergens))

        return knowledge_changed

    def _mark_dangers(self, ingredients: set[str], allergens: set[str]) -> None:
        """
        Mark a set of ingredients as dangerous, along with corresponding
          allergens

        Note that for sets with more than 1 element, no 1-to-1
          relationship can be directly inferred, but there must exist some
          1-to-1 relationship between the two sets

        For the reason above, the length of the two sets must equal

        Args:
            ingredients (set[str]):
                Set of ingredients known to be dangerous
            allergens   (set[str]):
                Set of allergens corresponding to the ingredients
        """
        # Sanity check
        if len(ingredients) != len(allergens):
            raise ValueError(
                f"Danger marking: # of ingredients not equal to # of allergens: "
                f"{ingredients} => {allergens}"
            )

        # Update dangers storage
        self.dangers.mark_dangers(ingredients, allergens)

        # If new individual mapping present, update each sentence about the
        #   danger
        known_allergens, known_ingredients = self.dangers.new_individual_maps()
        if not known_allergens:
            return

        for sentence in self.knowledge:
            sentence.mark_dangers(known_ingredients, known_allergens)
