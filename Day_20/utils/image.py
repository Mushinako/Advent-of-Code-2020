"""
Module: Image classes

Public Classes:
    ImagePiece    : A piece of image
    AssembledImage: The assembled image

Public Functions:
    concat_images: Concatenate images
"""

from __future__ import annotations

from functools import reduce
from operator import add, mul


class _BaseImage:
    """
    Image base class

    Args:
        data (list[str]): Original image piece

    Public Attributes:
        rotated_data (list[str]): Rotated image piece
        rotation     (int)      : Rotation indicator, a number 0-7, inclusive

    Public Methods:
        rotate: Rotate the image to the specified rotation
    """

    def __init__(self, data: list[str]) -> None:
        self._data = data
        self.rotated_data = list(self._data)
        self.rotation: int = 0

    def __repr__(self) -> str:
        rotated_data_repr = "\n    ".join(repr(row) for row in self.rotated_data)
        return (
            f"{self.__class__.__name__}(\n"
            f"  rotation={self.rotation},\n"
            f"  rotated_data=[\n"
            f"    {rotated_data_repr}\n"
            f"  ]\n"
            f")\n"
        )

    def rotate(self, rotation: int) -> None:
        """
        Rotate the image to the specified rotation

        Args:
            rotation (int): Rotation indicator, a number 0-7, inclusive
        """
        self.rotation = rotation
        copied_data = list(self._data)
        # 0-3 no flip; 4-7 vertical flip
        rotated_data = copied_data[::-1] if rotation >= 4 else copied_data
        # 0, 4: no rotation
        # 1, 5: clockwise rotation
        # 2, 6: 180° rotation
        # 3, 7: counterclockwise rotation
        i = rotation % 4
        if i == 1:
            self.rotated_data = ["".join(col[::-1]) for col in zip(*rotated_data)]
        elif i == 2:
            self.rotated_data = [row[::-1] for row in rotated_data[::-1]]
        elif i == 3:
            self.rotated_data = ["".join(col) for col in list(zip(*rotated_data))[::-1]]
        else:
            self.rotated_data = rotated_data


class ImagePiece(_BaseImage):
    """
    A piece of image

    Args:
        data (set[str]): Rotated image piece

    Public Attributes:
        unique_borders (set[str]): Set of unique borders this image has

    Public Read-only Properties:
        top     (str): Top border, from left to right
        bottom  (str)     : Bottom border, from left to right
        left    (str)     : Left border, from top to bottom
        right   (str)     : Right border, from top to bottom
        borders (set[str]): Set of all possible borders for this image piece

    Public Methods:
        borders_at: Get borders of a specific rotation without rotating the
                    image
    """

    def __init__(self, data: list[str]) -> None:
        super().__init__(data)
        self.unique_borders: set[str] = set()

    def __getitem__(self, k: str) -> str:
        """
        Allow attribute access via strings

        E.g., self["top"] instead of self.top
        """
        if k == "top":
            return self.top
        elif k == "bottom":
            return self.bottom
        elif k == "left":
            return self.left
        elif k == "right":
            return self.right
        else:
            raise KeyError(k)

    @property
    def top(self) -> str:
        return self.rotated_data[0]

    @property
    def bottom(self) -> str:
        return self.rotated_data[-1]

    @property
    def left(self) -> str:
        return "".join(row[0] for row in self.rotated_data)

    @property
    def right(self) -> str:
        return "".join(row[-1] for row in self.rotated_data)

    @property
    def borders(self) -> set[str]:
        borders = {self.top, self.bottom, self.left, self.right}
        return borders | {border[::-1] for border in borders}

    def borders_at(self, rotation: int) -> set[str]:
        """
        Get borders of a specific rotation without rotating the image

        Args:
            rotation (int): Rotation indicator, a number 0-7, inclusive

        Returns:
            (set[str]): Set of borders
        """
        new_self = ImagePiece(self._data)
        new_self.rotate(rotation)
        return {new_self.top, new_self.bottom, new_self.left, new_self.right}


class AssembledImage(_BaseImage):
    """
    The assembled image

    Public Class Methods:
        from_image_piece: Create instance from an image piece
    """

    def __add__(self, other: AssembledImage) -> AssembledImage:
        """
        Horizontal concatenation
        """
        assert len(self.rotated_data) == len(other.rotated_data)
        data = [
            self_row + other_row
            for self_row, other_row in zip(self.rotated_data, other.rotated_data)
        ]
        return AssembledImage(data)

    def __mul__(self, other: AssembledImage) -> AssembledImage:
        """
        Vertical concatenation
        """
        assert len(self.rotated_data[0]) == len(other.rotated_data[0])
        data = self.rotated_data + other.rotated_data
        return AssembledImage(data)

    @classmethod
    def from_image_piece(cls, image: ImagePiece) -> AssembledImage:
        """
        Create instance from an image piece

        Args:
            image (ImagePiece): Image piece to be assembled

        Returns:
            (AssembledImage): Image piece ready to be assembled
        """
        data = image.rotated_data
        last_row = len(data) - 1
        last_col = len(data[0]) - 1
        return cls([data[r][1:last_col] for r in range(1, last_row)])


def concat_images(
    all_images: dict[int, ImagePiece], solution_map: list[list[int]]
) -> AssembledImage:
    """
    Concatenate images

    For each image in one row, "add" the pieces to concatenate horizontally, and
      then "mul" the pieces to concatenate the rows vertically

    Args:
        all_images   (dict[int, ImagePiece]): All image pieces
        solution_map (list[list[int]])      : Solved map containing IDs

    Returns:
        (AssembledImage): Full image piece
    """
    assert len(solution_map) > 0
    # Concat all rows
    return reduce(
        mul,
        (
            # Concat each row
            # `sum` seems a little wonky here
            reduce(
                add, (AssembledImage.from_image_piece(all_images[id_]) for id_ in row)
            )
            for row in solution_map
        ),
    )
