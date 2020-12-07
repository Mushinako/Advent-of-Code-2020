# [Day 07: Handy Haversacks](https://adventofcode.com/2020/day/7)

## Part 1

The most difficult part of this problem is probably parsing the rules. While you
can go all out with regex, I decided to mix in a little `str.split` for easier
syntax.

```py
CHILDREN_COLOR_REGEX = re.compile(r"^\d+ (?P<color>.+) bags?$")

root_color, children = line.split(" bags contain ")
if children == "no other bags.":
    continue
for child in children[:-1].split(", "):
    color_match = CHILDREN_COLOR_REGEX.fullmatch(child)
    color = color_match["color"]
```

Once the input is parsed, the hierachy is used to create a mapping that maps a
specific color to the colors that contain it. E.g., given the example rule:

```txt
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
```

The mapping would look like:

```py
{
    'bright white': {'light red', 'dark orange'},
    'dark olive': {'shiny gold'},
    'dotted black': {'dark olive', 'vibrant plum'},
    'faded blue': {'dark olive', 'vibrant plum', 'muted yellow'},
    'muted yellow': {'light red', 'dark orange'},
    'shiny gold': {'bright white', 'muted yellow'},
    'vibrant plum': {'shiny gold'},
}
```

Then what's left is to walk through the nodes. Treating `shiny gold` as the root
and check how many nodes are below it. I chose something resembling
[`depth-first search`](https://en.wikipedia.org/wiki/Depth-first_search):

```py
stack = ["shiny gold"]
available_colors = set()

while stack:
    color = stack.pop()  # LIFO, depth-first
    outer_colors = map_[color]
    new_colors = outer_colors - available_colors
    available_colors |= outer_colors
    stack += list(new_colors)
```

## Part 2

This time, the question is about children and not parent, so the mapping is in
the other direction. It now maps each color to the colors within, along with
counts. E.g., for the same example rule above:

```txt
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
```

The new mapping would be like:

```py
{
    'light red': {'bright white': 1, 'muted yellow': 2},
    'dark orange': {'bright white': 3, 'muted yellow': 4},
    'bright white': {'shiny gold': 1},
    'muted yellow': {'shiny gold': 2, 'faded blue': 9},
    'shiny gold': {'dark olive': 1, 'vibrant plum': 2},
    'dark olive': {'faded blue': 3, 'dotted black': 4},
    'vibrant plum': {'faded blue': 5, 'dotted black': 6},
}
```

Once the tree is parsed, the actual counting is handled rather similarly to that
of part 1, the only caveat being the addition of a multiplying factor that's the
number of parent suitcases needed. While `dict` is not a good stack, I chose it
for its `__missing__` feature (`defaultdict`):

```py
stack: defaultdict[str, int] = defaultdict(lambda: 0)
stack["shiny gold"] = 1
total_count = 0

while stack:
    parent_color = next(iter(stack))
    parent_count = stack[parent_color]
    del stack[parent_color]
    rules = map_[parent_color]
    for child_color, child_count in rules.items():
        mul_child_count = parent_count * child_count
        total_count += mul_child_count
        stack[child_color] += mul_child_count
```
