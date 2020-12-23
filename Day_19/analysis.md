# [Day 19: Monster Messages](https://adventofcode.com/2020/day/19)

## Part 1

I  went for the approach converting each rule to regex, wrapping each one in a
group. E.g., for input:

```text
1: 2 3
2: 3 | 4
3: "a"
4: "b"
```

The rules are parsed as:

```py
{
    1: r'(("a") | ("b"))("a")',
    2: r'(("a") | ("b"))',
    3: r'("a")',
    4: r'("b")',
}
```

Simple substritutions (`str.replace`) do the job well.

## Part 2

While the method from part 1 technically works, sometime later I encountered
[catastrophic backtracking](https://www.regular-expressions.info/catastrophic.html).
For that, I decided to get some help from grammar parsing tools, such as `nltk`
and `lark`.

```py
def level2() -> int:
    """
    Level 2 solution

    Returns:
        (int): Solution to the problem
    """
    rules, texts = _read_input()
    parser = Lark(rules)

    result = 0
    for text in texts:
        try:
            parser.parse(text)
        except LarkError:
            # Not a solution
            continue
        else:
            result += 1
    return result
```

Note that this method works for part 1 as well and probably considerably
simpler than my current implementation.
