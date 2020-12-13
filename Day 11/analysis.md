# [Day 08: Handheld Halting](https://adventofcode.com/2020/day/8)

## Part 1

Brute-force approach is taken here, although the solution takes about half a
minute to run. During each iteration, the neighbors are checked, with
out-of-bounds ones ignored. Caching
([dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)) is
used to cache neighbor coordinates.

```py
def get_neighbor_occupied(
    map_: list[list[str]], neighbors: list[tuple[int, int]]
) -> int:
    count = sum(map_[r][c] == "#" for r, c in neighbors)
    return count

@cache
def get_neighbors(row: int, col: int) -> list[tuple[int, int]]:
    neighbors = [
        (r, c)
        for r, c in product(range(row - 1, row + 2), range(col - 1, col + 2))
        if 0 <= r < height and 0 <= c < width and (r != row or c != col)
    ]
    return neighbors
```

## Part 2

The major difference here is in the neighbor checking function. Instead of
checking immediate neighbors, it walks in each direction until it encounters a
seat or the edge of the map.

```py
directions = [(r, c) for r in range(-1, 2) for c in range(-1, 2) if r or c]

def get_neighbor_occupied(map_: list[list[str]], coord: tuple[int, int]) -> int:
    row, col = coord
    count = 0
    for dr, dc in directions:
        r = row
        c = col
        while 0 <= (r := r + dr) < height and 0 <= (c := c + dc) < width:
            if map_[r][c] == ".":
                continue
            if map_[r][c] == "#":
                count += 1
            break
    return count
```
