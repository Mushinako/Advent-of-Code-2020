#!/usr/bin/env python3
"""
Solution to part 2
"""
from __future__ import annotations
from math import prod
from itertools import product
from pathlib import Path
from typing import Optional

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


class _Rule:
    """
    A rule, storing rule name and ranges and provides a method to check validity

    Args:
        name   (str)           : Name of the rule
        ranges (frozenset[int]): Set of [start, end] pairs

    Instance Attributes:
        name       (str)           : Name of the rule
        ranges     (frozenset[int]): Set of [start, end] pairs
        valid_cols (set[_Column])  : Set of columns that satisfy this rule
        valid_col_count (int)      : Number of columns that satisfy this rule
        valid_col_ids   (list[int]): List of ids of columns that satisfy this
                                     rule

    Instance Methods:
        add_valid(_Column) -> None: Add column to `.valid_cols` if it satisfies
                                    this rule
        remove(_Column) -> None   : Remove column from `.valid_cols`, if exists
    """

    def __init__(self, name: str, ranges: frozenset[int]):
        if self.__class__ != _Rule:
            raise TypeError(f"_Rule class cannot be subclassed")
        self.name = name
        self.ranges = ranges
        self.valid_cols: set[_Column] = set()

    @property
    def valid_col_count(self) -> int:
        return len(self.valid_cols)

    # DEBUG
    @property
    def valid_col_ids(self) -> list[int]:
        return sorted(col.id_ for col in self.valid_cols)

    def add_valid(self, column: _Column) -> None:
        """
        Check if given column satisfies this rule. If so, add to the set of
          valid columns, and add the rule to the set of rules the column
          satisfies

        Args:
            column (_Column): The column of numbers to be checked
        """
        if column.values <= self.ranges:
            self.valid_cols.add(column)
            column.satisfied_rules.add(self)

    def remove(self, column: _Column) -> None:
        """
        Remove given column from valid columns and remove rule from column's
          satisfied rules

        Args:
            column (_Column): The column of numbers to be checked
        """
        if column in self.valid_cols:
            self.valid_cols.remove(column)
        if self in column.satisfied_rules:
            column.satisfied_rules.remove(self)


class _Column:
    """
    A column, storing column id and value set

    Args:
        id_             (int)           : The column id
        values          (frozenset[int]): Set of values in the column
        satisfied_rules (set[_Rule])    : Set of rules this column satisfy
        satisfied_rule_count (int)      : Number of rules this column satisfy
        satisfied_rule_names (list[str]): List names of rules this column satisfy

    Instance Attributes:
        id_    (int)           : The column id
        values (frozenset[int]): The set of values in the column

    Instance Methods:
        satisfies(_Rule) -> None: Add rule to `.satisfied_rules` if it matches
                                  this column
        remove(_Rule) -> None   : Remove rule from `.satisfied_rules`, if exists
    """

    def __init__(self, id_: int, values: frozenset[int]):
        if self.__class__ != _Column:
            raise TypeError(f"_Column class cannot be subclassed")
        self.id_ = id_
        self.values = values
        self.satisfied_rules: set[_Rule] = set()

    @property
    def satisfied_rule_count(self) -> int:
        return len(self.satisfied_rules)

    # DEBUG
    @property
    def satisfied_rule_names(self) -> list[str]:
        return sorted(rule.name for rule in self.satisfied_rules)

    def satisfies(self, rule: _Rule) -> None:
        """
        Check if this column satisfies a given rule. If so, add to the set of
          satisfied rules, and add the column to the set of columns the rule
          satisfies

        Args:
            rule (_Rule): The rule to be checked
        """
        rule.add_valid(self)

    def remove(self, rule: _Rule) -> None:
        """
        Remove given rule from satisfied rules and remove column from rule's
          valid columns

        Args:
            rule (_Rule): The rule to be checked
        """
        rule.remove(self)


class _RuleColumnMap:
    """
    Records found maps from rule to column ID, with some other helper methods

    Public Attributes:
        map_ (dict[str, int]): Map of rule name to column ID

    Public Methods:
        add_singles(dict[str, _Rule], dict[int, _Column]) -> bool:
            Add rules with only 1 matching column and columns with only 1
              matching rule
    """

    def __init__(self):
        self.map_: dict[str, int] = {}

    def add_singles(self, rules: dict[str, _Rule], cols: dict[int, _Column]) -> bool:
        """
        Add rules with only 1 matching column and columns with only 1 matching
          rule

        Args:
            rules (dict[str, _Rule])  : A collection of rules to be checked
            cols  (dict[int, _Column]): A collection of columns to be checked

        Returns:
            (bool): Whether any changes are made
        """
        rules_added = self._add_single_rules(rules, cols)
        cols_added = self._add_single_cols(cols, rules)
        return rules_added or cols_added

    def _add_single_rules(
        self, rules: dict[str, _Rule], cols: dict[int, _Column]
    ) -> bool:
        """
        Add rules with only 1 matching column

        Args:
            rules (dict[str, _Rule])  : A collection of rules to be checked
            cols  (dict[int, _Column]): A collection of columns

        Returns:
            (bool): Whether any changes are made
        """
        added_rules: set[_Rule] = set()
        added_cols: set[_Column] = set()
        for rule in rules.values():
            if rule.valid_col_count > 1:
                continue
            if not rule.valid_col_count:
                raise ValueError(f"{rule.name} has no matching columns")
            col = rule.valid_cols.pop()
            self.map_[rule.name] = col.id_
            added_rules.add(rule)
            added_cols.add(col)
        for rule in added_rules:
            del rules[rule.name]
        for rule in rules.values():
            rule.valid_cols -= added_cols
        for col in added_cols:
            del cols[col.id_]
        for col in cols.values():
            col.satisfied_rules -= added_rules
        return bool(added_rules)

    def _add_single_cols(
        self, cols: dict[int, _Column], rules: dict[str, _Rule]
    ) -> bool:
        """
        Add columns with only 1 matching rule

        Args:
            cols  (dict[int, _Column]): A collection of columns to be checked
            rules (dict[str, _Rule])  : A collection of rules

        Returns:
            (bool): Whether any changes are made
        """
        added_cols: set[_Column] = set()
        added_rules: set[_Rule] = set()
        for col in cols.values():
            if col.satisfied_rule_count > 1:
                continue
            if not col.satisfied_rule_count:
                raise ValueError(f"{col.id_} has no matching rules")
            rule = col.satisfied_rules.pop()
            self.map_[rule.name] = col.id_
            added_cols.add(col)
            added_rules.add(rule)
        for col in added_cols:
            del cols[col.id_]
        for col in cols.values():
            col.satisfied_rules -= added_rules
        for rule in added_rules:
            del rules[rule.name]
        for rule in rules.values():
            rule.valid_cols -= added_cols
        return bool(added_cols)


def _read_input() -> tuple[dict[str, _Rule], list[int], dict[int, _Column]]:
    """
    Read and parse the input file

    Returns:
        (dict[str, _Rule]): Rule name-valid values mapping
        (list[int])       : Your ticket
        (list[_Column])   : List of nearby valid tickets, organized by column
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        # Rules
        rule_nums = set()
        rules: dict[str, _Rule] = {}
        while (line := fp.readline().strip()) :
            name, rules_str = line.split(": ")
            ranges: set[int] = set()
            for rule in rules_str.split(" or "):
                start, end = rule.split("-")
                ranges |= set(range(int(start), int(end) + 1))
            rule = _Rule(name, frozenset(ranges))
            rules[rule.name] = rule
            rule_nums |= rule.ranges
        # Your ticket
        fp.readline()
        your_ticket = [int(n) for n in fp.readline().strip().split(",")]
        # Nearby tickets
        for _ in range(2):
            fp.readline()
        nearby_tickets: list[list[int]] = []
        for line in fp:
            ticket = [int(n) for n in line.strip().split(",")]
            if all(num in rule_nums for num in ticket):
                nearby_tickets.append(ticket)
        ticket_cols = {
            i: _Column(i, frozenset(col)) for i, col in enumerate(zip(*nearby_tickets))
        }

    return rules, your_ticket, ticket_cols


def _initialize(rules: dict[str, _Rule], cols: dict[int, _Column]) -> None:
    """
    Initialize mapping. Check each rule against each column

    Args:
        rules (dict[str, _Rule])  : Rule name-valid values mapping
        cols  (dict[int, _Column]): List of nearby valid tickets, organized by
                                    column
    """
    for rule, col in product(rules.values(), cols.values()):
        rule.add_valid(col)


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    rules, your_ticket, cols = _read_input()

    _initialize(rules, cols)

    rule_column_map = _RuleColumnMap()

    while rule_column_map.add_singles(rules, cols):
        pass

    # The dataset should be well-crafted such that `rules` and `cols` should be
    #   empty
    if rules:
        rules_residual = {rule.name: rule.valid_col_ids for rule in rules.values()}
        raise ValueError(f"rules not empty: {rules_residual}")
    if cols:
        cols_residual = {col.id_: col.satisfied_rule_names for col in cols.values()}
        raise ValueError(f"cols not empty: {cols_residual}")

    indices = (
        i
        for rule_name, i in rule_column_map.map_.items()
        if rule_name.startswith("departure")
    )
    return prod(your_ticket[i] for i in indices)


result = level2()

print(result)
print(submit_output(2020, 16, 2, result))