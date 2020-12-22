"""
Module: Everything about the sea monster

Public Functions:
    find_sea_monster_habitat: Find habitat roughness of the sea monster
"""

from itertools import product
from typing import Optional

from .image import AssembledImage


def find_sea_monster_habitat(image: AssembledImage) -> Optional[int]:
    """
    Find habitat roughness of the sea monster

    Args:
        image (AssembledImage): The full assembled image

    Returns:
        (int | None): Roughness score; `None` if no sea monsters are identified
    """
    sea_monster = _SeaMonster(_SEA_MONSTER_MAP)
    num_occupied = sum(row.count("#") for row in image.rotated_data)

    # Check all 8 rotations of the assembled map
    for i in range(8):
        image.rotate(i)
        image_content = list(image.rotated_data)
        row_count = len(image_content) - sea_monster.row_count + 1
        col_count = len(image_content[0]) - sea_monster.col_count + 1
        all_coords: set[tuple[int, int]] = set()

        # Check each cell that the sea monster occupies
        for row, col in product(range(row_count), range(col_count)):
            coords: set[tuple[int, int]] = set()
            for dr, dc in sea_monster.coords:
                r = row + dr
                c = col + dc
                if image_content[r][c] != "#":
                    break
                coords.add((r, c))
            else:
                all_coords |= coords

        if not all_coords:
            continue
        return num_occupied - len(all_coords)

    # Not found
    return None


_SEA_MONSTER_MAP = [
    "                  O ",
    "O    OO    OO    OOO",
    " O  O  O  O  O  O   ",
]


class _SeaMonster:
    """
    Pseudo-dataclass containing all information about the sea monster

    Args:
        sea_monster_map (list[str])

    Public Properties:
        row_count (int): Number of rows in the sea monster map
        col_count (int): Number of columns in the sea monster map
        coords    (list[tuple[int, int]]):
            List of coordinates of the sea monster
    """

    def __init__(self, sea_monster_map: list[str]):
        self.row_count = len(sea_monster_map)
        self.col_count = len(sea_monster_map[0])
        self.coords: list[tuple[int, int]] = [
            (r, c)
            for r, c in product(range(self.row_count), range(self.col_count))
            if sea_monster_map[r][c] == "O"
        ]
