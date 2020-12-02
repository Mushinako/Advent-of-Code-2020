# [Day 01: Report Repair](https://adventofcode.com/2020/day/1)

## Part 1

Wow isn't that the common problem of finding two numbers that sum up to a specific
value? We can try to be efficient here by just using `set`s, whose `in` check only
takes `O(1)` time! What we can do here is to iterate through all the numbers
(`O(n)`), calculate the number it requires to sum to 2020, and check if that
number is present (`O(1)`), with an overall time complexity of `O(n)`.

```py
# `data` is a `set`
for num in data:
    comp = goal - num
    if comp in data:
        ...
```

## Part 2

The 2nd part is basically the same, albeit one more variable and therefore one more
loop. Of course, I could've done 2 `for`-loops:

```py
# `data_list` is a `list` version of `data`, which is a `set`
for i, num1 in enumerate(data_list):
    for num2 in data_list[i+1:]:
        comp = goal - num1 - num2
        if comp > 0 and comp in data:
            ...
```

But why not be fancy and use `itertools.combinations` to achieve the same task? It
also has the added "benefit" of hiding the `O(n^2)` double `for`-loop.

```py
# `data` is a `set`
for num1, num2 in combinations(data, 2):
    comp = goal - num1 - num2
    if comp > 0 and comp in data:
        ...
```
