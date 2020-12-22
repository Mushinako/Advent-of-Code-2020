# [Day 20: Jurassic Jigsaw](https://adventofcode.com/2020/day/20)

## Part 1

Think about how the full map may look like (4×4 as an example):

```text
xxxxxxxxxxxxxxxxx
x   |   |   |   x
x A |   |   | B x
x   |   |   |   x
x---+---+---+---x
x   |   |   |   x
x   |   |   |   x
x   |   |   |   x
x---+---+---+---x
x   |   |   |   x
x   |   |   |   x
x   |   |   |   x
x---+---+---+---x
x   |   |   |   x
x C |   |   | D x
x   |   |   |   x
xxxxxxxxxxxxxxxxx
```

A special property of the corner pieces above `ABCD` is that they all have 2
sides that are not shared with other pieces. Therefore, if we find a piece that
has 2 sides that are not present on other pieces, it has to be a corner.

Note that the condition is
[**necessary** but not **sufficient**](https://en.wikipedia.org/wiki/Necessity_and_sufficiency);
i.e., a corner cell *may* have fewer than 2 unique sides due to collision. In
our case, however, the test case seems well-constructed to avoid that.

```py
def _get_corners(images: dict[int, Image]) -> set[int]:
    """
    Get corners of the map

    The corners are identified by comparing the sides of each image to those of
      other images. If 2 sides of an image are not present on any other image,
      then it has to be a corner.

    Note that this is not an all-encompassing method. This only works because
      the test cases are constructed for this.

    Args:
        images (dict[int, Image]): ID-image content mapping

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
            borders = set(image.borders_at(i).values())
            left = borders - other_image_borders
            if len(left) == 2:
                corners.add(id_)
                break

    return corners
```

## Part 2

Brute-forcing the rest is still quite resource-intensive. We can utilize the
method from [Part 1](#part-1) for a step further; this time, find the pieces
with 1 unique side, which would be the sides. Note that again, this condition
is **necessary** but not **sufficient**.

The rest of the match are pretty-much done with brute-force. For each cell,
iterate through each possible choice of pieces and rotate them into each of the
8 possible orientations. Check if it works well with other pieces present. If
so, continue; else, backtrack. I personally chose to do this recursively, given
the recursion depth is only about 100 for the given input and can be tail-call
optimized if really wanted to.
