"""
Module: Miscellaneous utility functions

Public Functions:
    check_cell_valid: Check if a given cell fits its surroundings
"""

from .image import ImagePiece


def check_cell_valid(
    all_images: dict[int, ImagePiece],
    assembled_map: list[list[int]],
    image: ImagePiece,
    row: int,
    col: int,
) -> bool:
    """
    Check if a given cell fits its surroundings

    Args:
        all_images    (dict[int, ImagePiece]): ID-image mapping of all images
        assembled_map (list[list[int]])      : Map canvas with parts filled
        image         (Image)                : The image to be checked
        row           (int)                  : Row index of the image
        col           (int)                  : Column index of the image
    """
    last_row = len(assembled_map) - 1
    last_col = len(assembled_map[0]) - 1

    # Check top
    if (
        row != 0
        and (top_id := assembled_map[row - 1][col]) != -1
        and all_images[top_id].bottom != image.top
    ):
        return False

    # Check bottom
    if (
        row != last_row
        and (bottom_id := assembled_map[row + 1][col]) != -1
        and all_images[bottom_id].top != image.bottom
    ):
        return False

    # Check left
    if (
        col != 0
        and (left_id := assembled_map[row][col - 1]) != -1
        and all_images[left_id].right != image.left
    ):
        return False

    # Check right
    if (
        col != last_col
        and (right_id := assembled_map[row][col + 1]) != -1
        and all_images[right_id].left != image.right
    ):
        return False

    # All checks passed
    return True
