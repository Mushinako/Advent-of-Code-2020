#!/usr/bin/env python3
"""
Solution to part 2
"""
import re
from pathlib import Path
from typing import Optional

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_20.utils.image import ImagePiece, concat_images
from Day_20.utils.corners import allocate_corners
from Day_20.utils.sides import allocate_sides, gen_side_coords
from Day_20.utils.rest import allocate_rest, gen_rest_coords
from Day_20.utils.sea_monster import find_sea_monster_habitat

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> dict[int, ImagePiece]:
    """
    Read and parse the input file

    Returns:
        (dict[int, ImagePiece]): ID-image mapping of all images
    """
    tile_re = re.compile(r"Tile (\d+):")
    images: dict[int, ImagePiece] = {}

    id_: Optional[int] = None
    data: list[str] = []

    with _INPUT_FILE_PATH.open("r") as fp:
        for l in fp:
            line = l.strip()
            if not line:
                assert id_ and data
                images[id_] = ImagePiece(data)
                id_ = None
                data = []
            elif (match := tile_re.fullmatch(line)) is not None:
                id_ = int(match[1])
            else:
                data.append(line)
        if id_ and data:
            images[id_] = ImagePiece(data)
            id_ = None
            data = []

    return images


def _get_corners_sides(images: dict[int, ImagePiece]) -> tuple[set[int], set[int]]:
    """
    Get corners and sides of the map

    The corners are identified by comparing the sides of each image to those of
      other images. If 2 sides of an image are not present on any other image,
      then it has to be a corner. Similarly, if only 1 side of an image is
      unique, then the image has to be on the side

    Note that this is not an all-encompassing method. This only works because
      the test cases are constructed for this.

    Args:
        images (dict[int, ImagePiece]): ID-image mapping of all images

    Returns:
        (set[int]): Set of IDs of images that are corners
        (set[int]): Set of IDs of images that are sides
    """
    corners: set[int] = set()
    sides: set[int] = set()

    # Check each image against all other images
    for id_, image in images.items():
        other_image_borders = {
            border
            for id__, image_ in images.items()
            if id__ != id_
            for border in image_.borders
        }

        # Check each rotation
        for i in range(8):
            left = image.borders_at(i) - other_image_borders
            # Corner has 2 unique sides
            if len(left) == 2:
                corners.add(id_)
                image.unique_borders = left
                break
            # Side has 1 unique side
            elif len(left) == 1:
                sides.add(id_)
                image.unique_borders = left
                break

    return corners, sides


def _solve_map(
    all_images: dict[int, ImagePiece],
    corner_ids: set[int],
    side_ids: set[int],
) -> Optional[list[list[int]]]:
    """
    Find a way to allocate all the images into the larger map

    Args:
        images     (dict[int, ImagePiece]): ID-image mapping of all images
        corner_ids (set[int])        : Set of IDs of images that are corners
        side_ids   (set[int])        : Set of IDs of images that are sides

    Returns:
        (list[list[int]] | None):
            Solution, presented as a 2D-list of image IDs. `None` is retured in
            case no solution is found.
    """
    square_side_len = round(len(all_images) ** 0.5)
    assert len(corner_ids) == 4 and len(side_ids) == 4 * (square_side_len - 2)

    # Categorize each image into corner, side, and the rest
    corner_images: dict[int, ImagePiece] = {}
    side_images: dict[int, ImagePiece] = {}
    other_images: dict[int, ImagePiece] = {}
    for id_, image in all_images.items():
        if id_ in corner_ids:
            corner_images[id_] = image
        elif id_ in side_ids:
            side_images[id_] = image
        else:
            other_images[id_] = image

    # Initiate a map and prefill with -1
    base_map = [[-1] * square_side_len for _ in range(square_side_len)]

    # Corners -> sides -> the rest
    for cornered_map in allocate_corners(corner_images, base_map):
        sided_map = allocate_sides(
            all_images,
            side_images,
            cornered_map,
            gen_side_coords(square_side_len, square_side_len),
        )
        if not sided_map:
            continue
        result = allocate_rest(
            all_images,
            other_images,
            sided_map,
            gen_rest_coords(square_side_len, square_side_len),
        )
        if not result:
            continue
        return result

    # No solution found
    return None


def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    all_images = _read_input()
    corners, sides = _get_corners_sides(all_images)
    solution_map = _solve_map(all_images, corners, sides)
    if not solution_map:
        raise ValueError("No solution")
    image = concat_images(all_images, solution_map)
    roughness = find_sea_monster_habitat(image)
    if not roughness:
        raise ValueError("No sea monsters identified")
    return roughness


if __name__ == "__main__":
    result = level2()
    print(result)
    print(submit_output(2020, 20, 2, result))
