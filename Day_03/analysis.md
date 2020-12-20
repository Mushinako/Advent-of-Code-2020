# [Day 03: Toboggan Trajectory](https://adventofcode.com/2020/day/3)

## Part 1

One critical insight for this problem is that you don't need to actually copy the
tree pattern. For a map of width `w`, notice that the pattern at `(row, col)` must
be the same as that at `(row, col mod w)`. If you know about group theory, you may
identify that the column pattern is a
[cyclic group of order `w`](https://en.wikipedia.org/wiki/Cyclic_group). But for
non-nerds, we'll just use `mod` and call it a day.

What's left is to get all the cells that match the 3-right-1-down rule, and a
`for` loop can take care of that easily.

```py
spaces = [map_[i][i * right % map_width] for i in range(len(map_))]
```

`i * right % map_width` first moves the toboggan right by `right` cells (`3` in
this case) and mods `map_width` to wrap in around.

### More explanation on the `mod`

For simplicity, let's reduce the number of rows to 2. Say I have a map like this:

```txt
012 (column indices, 0-based)
.#.
.##
```

Given that the pattern duplicates horizontally, the full pattern would be something like:

```txt
012345678... (column indices, 0-based)
.#..#..#.
.##.##.##
```

Let's say, I want to get the cell `(0, 8)` (roww 0, column 8). Notice how that's
the same as cell `(0, 2)`. This is because I can keep subtracting the width of the
original map, and `2` would be a remainder. In more formal terms, we'd call this
`8 ≡ 2 (mod 3)`. In Python, the mod opertor `%` does this job well.

```py
print(8 % 3)  # 2
```

## Part 2

The second part is almost as same as the first part, but one annoying thing is that
in the last case, each action goes down by 2 rows. The solution for part 1
basically works, albeit with some small modifications.

```py
spaces = [map_[i * down][i * right % map_width] for i in range(len(map_) // down)]
```

`i * down` moves the toboggan down by `down` rows (`1` or `2`). One tricky part is
to reduce the `range` according to how many rows that's covered each time, hence
the `len(map_) // down`.
