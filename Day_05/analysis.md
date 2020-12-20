# [Day 05: Binary Boarding](https://adventofcode.com/2020/day/5)

## Part 1

The boarding pass smells binary! Effectively, `B` and `R` are `1`, and `F` and `L`
are `0`. In Python, one can replace the characters with `0` and `1` and convert
the binary string to an integer.

```py
mapping = str.maketrans({"B": "1", "F": "0", "R": "1", "L": "0"})
seat_id = int(row_stripped.translate(mapping), 2)
```

The maximum can be got via the `max` function.

## Part 2

I took a brute-force approach to the second part, iterating through all the seat
IDs, checking that `seat_id + 1` is not present and `seat_id + 2` is present. A
`set` is utilized to take advantage of `O(1)` membership check, yielding an overall
`O(n)` time complexity.
