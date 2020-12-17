#!/usr/bin/env python3
"""
Solution to part 2
"""
import sys
from pathlib import Path
from collections import defaultdict
from itertools import product

from aoc_io.aoc_io import DATA_FILENAME, submit_output

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME

# 4D coordinates
_Coord = tuple[int, int, int, int]


class _Game:
    """
    4D Conway game
    The underlying board is a `defaultdict[_Coord, bool]`

    Args:
        initial_state (list[list[bool]]): Original 2D board

    Public Instance Attributes:
        board  (defaultdict[_Coord, bool]): Game board
        coords (set[_Coord])              : Set of active cell coords

    Public Instance Methods:
        propagate() -> None  : Construct the next generation
        count_active() -> int: Count the number of active cells
    """

    def __init__(self, initial_state: list[list[bool]]) -> None:
        self.board = self._create_board()
        self.coords = self._create_coord_set()
        for x, row in enumerate(initial_state):
            for y, cell in enumerate(row):
                if cell:
                    coord = (x, y, 0, 0)
                    self.board[coord] = cell
                    self.coords.add(coord)

    def propagate(self) -> None:
        """
        Construct the next generation
        """
        interesting_coods = self._create_coord_set()
        for coord in self.coords:
            if not self.board[coord]:
                continue
            x, y, z, w = coord
            interesting_coods |= set(
                product(
                    range(x - 1, x + 2),
                    range(y - 1, y + 2),
                    range(z - 1, z + 2),
                    range(w - 1, w + 2),
                )
            )
        new_board = self._create_board()
        new_coords = self._create_coord_set()
        for icoord in interesting_coods:
            if self.board[icoord]:
                if self._count_neighbors(icoord) in {2, 3}:
                    new_board[icoord] = True
                    new_coords.add(icoord)
            else:
                if self._count_neighbors(icoord) == 3:
                    new_board[icoord] = True
                    new_coords.add(icoord)
        self.board = new_board
        self.coords = new_coords

    def count_active(self) -> int:
        """
        Count the number of active cells

        Returns:
            (int): The number of active cells
        """
        return sum(self.board.values())

    def _count_neighbors(self, coord: _Coord) -> int:
        """
        Count the number of active neighbors

        Args:
            coord (_Coord): The coord to be checked

        Returns:
            (int): The number of active neighbors around the coord
        """
        x, y, z, w = coord
        all_sum = sum(
            self.board[icoord]
            for icoord in product(
                range(x - 1, x + 2),
                range(y - 1, y + 2),
                range(z - 1, z + 2),
                range(w - 1, w + 2),
            )
        )
        return all_sum - self.board[coord]

    @staticmethod
    def _create_board() -> defaultdict[_Coord, bool]:
        """
        Create an empty board; mainly for typing purposes

        Returns:
            (defaultdict[_Coord, bool]): Empty board
        """
        return defaultdict(lambda: False)

    @staticmethod
    def _create_coord_set() -> set[_Coord]:
        """
        Create a coord set; mainly for typing purposes

        Returns:
            (set[_Coord]): Empty coord set
        """
        return set()


def _read_input() -> list[list[bool]]:
    """
    Read and parse the input file

    Returns:
        (list[list[bool]]): Puzzle input
    """
    with _INPUT_FILE_PATH.open("r") as fp:
        lines = [
            [bool(char == "#") for char in line] for l in fp if (line := l.strip())
        ]

    return lines


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    initial_state = _read_input()
    game = _Game(initial_state)
    for i in range(1, 7):
        print(f"propagation #{i}", file=sys.stderr)
        game.propagate()
    return game.count_active()


result = level2()

print(result)
print(submit_output(2020, 17, 2, result))
