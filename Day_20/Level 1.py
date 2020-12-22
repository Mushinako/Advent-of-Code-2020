#!/usr/bin/env python3
"""
Solution to part 1
"""
import re
from math import prod
from pathlib import Path
from typing import Optional

from aoc_io.aoc_io import DATA_FILENAME, submit_output
from Day_20.utils.image import ImagePiece

_CURRENT_DIR = Path(__file__).resolve().parent
_INPUT_FILE_PATH = _CURRENT_DIR / DATA_FILENAME


def _read_input() -> dict[int, ImagePiece]:
    """
    Read and parse the input file

    Returns:
        (dict[int, ImagePiece]): All the image pieces
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


def _get_corners(images: dict[int, ImagePiece]) -> set[int]:
    """
    Get corners of the map

    The corners are identified by comparing the sides of each image to those of
      other images. If 2 sides of an image are not present on any other image,
      then it has to be a corner.

    Note that this is not an all-encompassing method. This only works because
      the test cases are constructed for this.

    Args:
        images (dict[int, ImagePiece]): ID-image content mapping

    Returns:
        (set[int]): Set of IDs of images that are corners
    """
    corners: set[int] = set()

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
            if len(left) == 2:
                corners.add(id_)
                break

    return corners


def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    images = _read_input()
    corners = _get_corners(images)
    if len(corners) != 4:
        raise ValueError(corners)
    return prod(corners)


if __name__ == "__main__":
    result = level1()
    print(result)
    print(submit_output(2020, 20, 1, result))
