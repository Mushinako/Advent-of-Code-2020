"""
Module: Process images in the corner

Public Functions:
    allocate_corners: Find valid corner allocations
"""

from itertools import permutations
from typing import Generator, Literal, Union

from .image import ImagePiece


def allocate_corners(
    corner_images: dict[int, ImagePiece],
    base_map: list[list[int]],
) -> Generator[list[list[int]], None, None]:
    """
    Find valid corner allocations

    Args:
        corner_images (dict[int, ImagePiece]):
            ID-image mapping of the 4 corner images
        base_map (list[list[int]]): Empty map canvas

    Yields:
        (list[list[int]]): Valid ID maps with corners filled
    """
    # We can fix one image; let's say top-left
    other_corner_ids = set(corner_images)
    top_left = other_corner_ids.pop()

    # Permute the possible choices for the other 3 corners, total `3! = 6`
    #   possibilities
    for top_right, bottom_left, bottom_right in permutations(other_corner_ids):
        copied_map = [list(row) for row in base_map]
        top_left_image = corner_images[top_left]
        top_right_image = corner_images[top_right]
        bottom_left_image = corner_images[bottom_left]
        bottom_right_image = corner_images[bottom_right]
        copied_map[0][0] = top_left
        copied_map[0][-1] = top_right
        copied_map[-1][0] = bottom_left
        copied_map[-1][-1] = bottom_right

        # Try all valid rotations for each corner, total `2**4 = 16`
        #   possibilities
        # Can't `itertools.product` here because the images are manipulated
        for _ in _rotate_corner(top_left_image, "top_left"):
            for _ in _rotate_corner(top_right_image, "top_right"):
                for _ in _rotate_corner(bottom_left_image, "bottom_left"):
                    for _ in _rotate_corner(bottom_right_image, "bottom_right"):
                        yield copied_map


def _rotate_corner(
    image: ImagePiece,
    position: Union[
        Literal["top_left"],
        Literal["top_right"],
        Literal["bottom_left"],
        Literal["bottom_right"],
    ],
) -> Generator[None, None, None]:
    """
    Rotate each corner image so that the correct sides are on the outside.
      These are its `unique_borders`. E.g., the `unique_borders` for the
      `top_left` corner has to be on the `top` and `left` of the piece

    This generator yields `None` because the image is rotated within this
      generator. The `yield` merely pauses the iteration through the rotations,
      "fixing" the current rotation

    Args:
        image (ImagePiece): Image object of the corner, to be rotated
        position (str)    : One of the corner positional strings, indicating
                            which corner this image should be in
    """
    # Valid border targets consist of the 2 target strings and their reverses
    targets = image.unique_borders | {t[::-1] for t in image.unique_borders}

    # Side names to be checked. E.g., the `top_left` corner checks the `top`
    #   border and the `left` border
    side1_name, side2_name = position.split("_")

    # Iterate through each rotation and check whether the correct sides are
    #   on the outside
    for i in range(8):
        image.rotate(i)
        check = {image[side1_name], image[side2_name]}
        if check < targets:
            yield
