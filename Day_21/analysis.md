# [Day 18: Operation Order](https://adventofcode.com/2020/day/18)

## Part 1

Brute-force implementation. All the `(...)`s are first evaluated, then the rest
are evaluated left-to-right.

### Part 1 but Smarter

As the operators only contain `+` and `*`, we can be a little more... risky. If
there's a way to bring `*` and `+` to the same precedence level, then the
problem is rather simple. In fact, there's already an unused operator that's at
the same level as `+`: `-`. Now what we have to do is to replace `*` with `-`
and override the `__sub__` with multiplication.

## Part 2

Almost the same as Part 1, with the difference that all `+`s in a formula
section are evaluated before `*`s.

### Part 2 but Smarter

Almost the same thing as Part 1, but this time replace `+` with `**` and
override `__pow__` with addition.
