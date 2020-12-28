# [Day 24: Lobby Layout](https://adventofcode.com/2020/day/24)

## Part 1

A hex grid can be represented by a sheered square grid:

```text
 a b         a b
f O c  =>  f O c
 e d       e d
```

```py
def level1() -> int:
    """
    Level 1 solution

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
    return sum(tiles_changed.values())
```

## Part 2

Another
[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life),
but this time in a hex grid! (Specifically, rule `H:B2/S12`)

```py
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
```
