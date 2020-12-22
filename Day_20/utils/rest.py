"""
Module: Process images not in the corners or on the sides

Public Functions:
    allocate_rest  : Find valid allocations for the images left
    gen_rest_coords: Generate coordinates not on the edge of the map
"""

from itertools import product
from typing import Generator, Optional

from .image import ImagePiece
from .utils import check_cell_valid


def allocate_rest(
    all_images: dict[int, ImagePiece],
    rest_images: dict[int, ImagePiece],
    assembled_map: list[list[int]],
    coords_gen: Generator[tuple[int, int], None, None],
) -> Optional[list[list[int]]]:
    """
    Find valid allocations for the images left

    Args:
        all_images  (dict[int, ImagePiece]):
            ID-image mapping of all images
        rest_images (dict[int, ImagePiece]):
            ID-image mapping of all images not allocated
        assembled_map (list[list[int]]):
            Map canvas with parts filled
        coords_gen (Generator[tuple[int, int]]):
            Coordinate generator, yields 2 integers as row-column coordinate

    Returns:
        (list[list[int]] | None):
            Valid ID maps with parts filled; `None` if no such valid map exists
    """
    # Resursion ends when all images are allocated
    if not len(rest_images):
        return assembled_map

    # Get coordinate
    row, col = next(coords_gen)

    # Iterate through all the images and try them
    for id_, image in rest_images.items():
        # Check each rotation for this image
        for i in range(8):
            image.rotate(i)
            if not check_cell_valid(all_images, assembled_map, image, row, col):
                continue
            copied_map = [list(row) for row in assembled_map]
            copied_map[row][col] = id_
            other_rest_images = {
                id__: image_ for id__, image_ in rest_images.items() if id__ != id_
            }
            result = allocate_rest(
                all_images, other_rest_images, copied_map, coords_gen
            )
            if result:
                return result

    # No solution found
    return None


def gen_rest_coords(
    row_count: int, col_count: int
) -> Generator[tuple[int, int], None, None]:
    """
    Generate coordinates not on the edge of the map

    Args:
        row_count (int): Number of rows in the map
        col_count (int): Number of columns in the map

    Yields:
        (int): Row index
        (int): Column index
    """
    last_row = row_count - 1
    last_col = col_count - 1

    yield from product(range(1, last_row), range(1, last_col))
