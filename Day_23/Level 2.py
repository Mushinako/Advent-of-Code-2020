#!/usr/bin/env python3
"""
Solution to part 2
"""

from __future__ import annotations

from pathlib import Path
from typing import Generator

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_23.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


class _Node:
    """
    A node within the linked list

    Args:
        value (int) : The value stored in the node
        next  (Node): Next Node in the linked list

    Public Attributes:
        value (int) : The value stored in the node
        next  (Node): Next Node in the linked list
    """

    def __init__(self, value: int):
        self.value = value
        self.next = self

    def __repr__(self) -> str:
        return f"Node({self.value})"


class _CircularLinkedList:
    """
    A circularly linked list of nodes

    Args:
        nums (list[int]): List of numbers to be converted to nodes

    Public Methods:
        crab_cups:
            One iteration of the crab-cups game
        star_prodcut:
            Get the 2 nodes after the node with value 1 and calculate their
            product
    """

    def __init__(self, nums: list[int]) -> None:
        nums_iter = iter(nums)
        # Create the first node
        first_num = next(nums_iter)
        first_node = _Node(first_num)
        # Create value-node mapping for `O(1)` average access
        self._value_node_map = {first_num: first_node}
        prev_node = first_node
        # For each new node thereafter, link it to the previous node, and add
        #   it to the mapping
        for n in nums_iter:
            new_node = _Node(n)
            self._value_node_map[n] = new_node
            prev_node.next = new_node
            prev_node = new_node
        # Link the last node to the first node
        prev_node.next = first_node
        # Initiate the current node as first node
        self._current_node = first_node
        # Store length
        self._length = len(nums)
        # Store maximum
        self._max = max(nums)

    def __iter__(self) -> _CircularLinkedList:
        self._iter_current_node = self._current_node
        self._iter_counter = 0
        return self

    def __next__(self) -> Generator[_Node, None, None]:
        while self._iter_counter < self._length:
            self._iter_counter += 1
            node = self._iter_current_node
            self._iter_current_node = node.next
            yield node

    def __getitem__(self, value: int) -> _Node:
        """
        Gets a Node by value
        """
        return self._value_node_map[value]

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        """
        Prints the first 10 elements and then ...
        """
        if self._length <= 10:
            content = ", ".join(str(n) for n in iter(self))
        else:
            iter_self = iter(self)
            content = ", ".join(str(next(iter_self)) for _ in range(10)) + ", ..."
        return f"CircularLinkedList({content})"

    def crab_cups(self) -> None:
        """
        One iteration of the crab-cups game
        """
        # Get the current node
        current_node = self._current_node
        # Get the next 3 nodes
        next_node = current_node.next
        next_next_node = next_node.next
        next_next_next_node = next_next_node.next
        # The next 3 values and 0 can't be the destination
        bad_nums = {
            0,
            next_node.value,
            next_next_node.value,
            next_next_next_node.value,
        }
        # Look for destination, from current value, `O(1)`
        dest_value = current_node.value
        while True:
            dest_value -= 1
            if not dest_value:
                dest_value = self._max
            if dest_value not in bad_nums:
                break
        # Get destination node, `O(1)` average
        dest_node = self._value_node_map[dest_value]
        # Remove the 3 elements, `O(1)`
        current_node.next = next_next_next_node.next
        # Add the 3 elements after destination, `O(1)`
        next_next_next_node.next = dest_node.next
        dest_node.next = next_node
        # Go to the next node, preparing for the next loop
        self._current_node = current_node.next

    def star_product(self) -> int:
        """
        Get the 2 nodes after the node with value 1 and calculate their product

        Returns:
            (int): The product
        """
        one_node_next = self._value_node_map[1].next
        return one_node_next.value * one_node_next.next.value


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    length = 1_000_000
    nums: list[int] = read_input(_INPUT_FILE_PATH) + list(range(10, length + 1))

    cups = _CircularLinkedList(nums)

    for _ in range(10_000_000):
        cups.crab_cups()
    return cups.star_product()


if __name__ == "__main__":
    result = level2()
    print(result)
    print(submit_output(2020, 23, 2, result))
