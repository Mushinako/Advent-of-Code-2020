# [Day 05: Binary Boarding](https://adventofcode.com/2020/day/5)

## Part 1

Once the problem asks for occurrence in *any* of something, `set.union` is your
friend:

```py
responses = set.union(*[set(person) for person in people])
```

## Part 2

Once the problem asks for occurrence in *all* of something, `set.intersection` is
your friend:

```py
responses = set.intersection(*[set(person) for person in people])
```
