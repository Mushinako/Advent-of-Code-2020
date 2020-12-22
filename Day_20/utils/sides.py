"""
Module: Process images on the side

Public Functions:
    allocate_sides : Find valid side allocations
    gen_side_coords: Generate coordinates on the edge of the map and is not a
                     corner
"""

from typing import Generator, Literal, Optional, Union

from .image import ImagePiece
from .utils import check_cell_valid


def allocate_sides(
    all_images: dict[int, ImagePiece],
    side_images: dict[int, ImagePiece],
    assembled_map: list[list[int]],
    coords_gen: Generator[
        tuple[
            int,
            int,
            Union[Literal["top"], Literal["bottom"], Literal["left"], Literal["right"]],
        ],
        None,
        None,
    ],
) -> Optional[list[list[int]]]:
    """
    Find valid corner allocations

    Args:
        all_images  (dict[int, ImagePiece]):
            ID-image mapping of all images
        side_images (dict[int, ImagePiece]):
            ID-image mapping of side images not allocated
        assembled_map (list[list[int]]):
            Map canvas with parts filled
        coords_gen (Generator[tuple[int, int, str]]):
            Coordinate generator, yields 2 integers as row-column coordinate
            and a string indicating which side it is on

    Returns:
        (list[list[int]] | None):
            Valid ID maps with parts filled; `None` if no such valid map exists
    """
    # Resursion ends when all side images are allocated
    if not side_images:
        return assembled_map

    # Get coordinate
    row, col, position = next(coords_gen)

    # Iterate through all the images and try them
    for id_, image in side_images.items():
        # Check each rotation for this image
        for _ in _rotate_side(image, position):
            if not check_cell_valid(all_images, assembled_map, image, row, col):
                continue
            copied_map = [list(row) for row in assembled_map]
            copied_map[row][col] = id_
            other_side_images = {
                id__: image_ for id__, image_ in side_images.items() if id__ != id_
            }
            result = allocate_sides(
                all_images, other_side_images, copied_map, coords_gen
            )
            if result:
                return result

    # No solution found
    return None


def gen_side_coords(
    row_count: int, col_count: int
) -> Generator[
    tuple[
        int,
        int,
        Union[Literal["top"], Literal["bottom"], Literal["left"], Literal["right"]],
    ],
    None,
    None,
]:
    """
    Generate coordinates on the edge of the map and is not a corner

    Args:
        row_count (int): Number of rows in the map
        col_count (int): Number of columns in the map

    Yields:
        (int): Row index
        (int): Column index
        (str): Position string
    """
    last_row = row_count - 1
    last_col = col_count - 1

    # Weave coordinates on the left and right
    # E.g., (1, 0), (1, last_col), (2, 0), (2, last_col), ...
    for r in range(1, last_row):
        yield r, 0, "left"
        yield r, last_col, "right"

    # Weave coordinates on the top and bottom
    # E.g., (0, 1), (last_row, 1), (0, 2), (last_row, 2), ...
    for c in range(1, last_col):
        yield 0, c, "top"
        yield last_row, c, "bottom"


def _rotate_side(
    image: ImagePiece,
    position: Union[
        Literal["top"],
        Literal["bottom"],
        Literal["left"],
        Literal["right"],
    ],
) -> Generator[None, None, None]:
    """
    Rotate each side image so that the correct side is on the outside. This is
      the only element of its `unique_borders`. E.g., the `unique_borders` for
      a side image on the `right` has to point to the `right`

    This generator yields `None` because the image is rotated within this
      generator. The `yield` merely pauses the iteration through the rotations,
      "fixing" the current rotation

    Args:
        image (ImagePiece): Image object of the side, to be rotated
        position (str)    : One of the side positional strings, indicating which
                            side this image should be on
    """
    # Valid side targets consist of the target string and its reverse
    (side,) = image.unique_borders
    targets = {side, side[::-1]}

    # Iterate through each rotation and check whether the correct side is on
    #   the outside
    for i in range(8):
        image.rotate(i)
        check = image[position]
        if check in targets:
            yield
