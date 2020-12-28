#!/usr/bin/env python3
"""
Solution to part 2
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_24.utils.read_input import read_input

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


class HexGameOfLife:
    """
    Conway's Game of Life, but in a hex grid! (Rule H:B2/S12)

    Instance Public Attributes:
        board (set[complex]): Set of coordinates where the tile is black

    Instance Public Read-Only Properties:
        black_tiles_count (int): Number of black tile counts
    """

    def __init__(self, initial_board: dict[complex, bool]) -> None:
        self.board = {coord for coord, black in initial_board.items() if black}

    @property
    def black_tiles_count(self) -> int:
        return len(self.board)

    def propagate(self) -> None:
        """
        Run one round of propagation
        """
        sus_poses: set[complex] = set()
        for black_pos in self.board:
            sus_poses.add(black_pos)
            sus_poses |= self.gen_neighbors(black_pos)
        new_board: set[complex] = set()
        for sus_pos in sus_poses:
            neighbors_black = sum(
                pos in self.board for pos in self.gen_neighbors(sus_pos)
            )
            if sus_pos in self.board:
                # Black
                if neighbors_black in {1, 2}:
                    new_board.add(sus_pos)
            else:
                # White
                if neighbors_black == 2:
                    new_board.add(sus_pos)
        self.board = new_board

    @staticmethod
    def gen_neighbors(pos: complex) -> set[complex]:
        """
        Get set of coordinate of neighbors of a coordinate
        """
        return {pos + 1, pos - 1, pos + 1j, pos - 1j, pos + 1 + 1j, pos - 1 - 1j}


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    instructions = read_input(_INPUT_FILE_PATH)
    tiles_changed: defaultdict[complex, bool] = defaultdict(lambda: False)
    for instruction in instructions:
        coord = 0 + 0j
        for step in instruction:
            if step == "e":
                coord += 1
            elif step == "w":
                coord -= 1
            elif step == "nw":
                coord += 1j
            elif step == "se":
                coord -= 1j
            elif step == "ne":
                coord += 1 + 1j
            elif step == "sw":
                coord -= 1 + 1j
            else:
                raise ValueError(f"Unknown step: {step}")
        tiles_changed[coord] ^= True
    hex_game_of_life = HexGameOfLife(tiles_changed)
    for _ in range(100):
        hex_game_of_life.propagate()
    return hex_game_of_life.black_tiles_count


if __name__ == "__main__":
    result = level2()
    print(result)
    print(submit_output(2020, 24, 2, result))
