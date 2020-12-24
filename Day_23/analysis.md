# [Day 23: Crab Cups](https://adventofcode.com/2020/day/23)

## Part 1

This part is small enough to be brute-forced, so brute-force it is!

```py
def level1() -> str:
    """
    Level 1 solution

    Returns:
        (str): Solution to the problem
    """
    cups: list[int] = read_input(_INPUT_FILE_PATH)
    max_ = max(cups)
    for _ in range(100):
        # Current element
        current = cups[0]
        # Elements not touched this loop
        left = cups[4:]
        left_set = set(left)
        # Find the next smallest value in the numbers left; wrap around to
        #   `max_` if the value decreases to 0
        while True:
            current -= 1
            if not current:
                current = max_
            if current in left_set:
                break
        # Add the 3 cups after the destination value, and then move the current
        #   value to the end of the list
        dest_index = cups.index(current) + 1
        cups = cups[4:dest_index] + cups[1:4] + cups[dest_index:] + cups[:1]
    index_1 = cups.index(1)
    return "".join(str(n) for n in (cups[index_1 + 1 :] + cups[:index_1]))
```

## Part 2

I tried my brute-force implementation and it took a whopping 57 minutes on my
machine! While that does give the right answer, clearly we have to do better.

The shortcomings of my current implementation are the `list.index()` and list
slicing `[start:end]`, both of which takes `O(n)` to complete. Are there ways to
make them more efficient?

What I come up with is basically my own version of singly-linked circular list,
with the end of the list linked to the front as well.

```py
def crab_cups(self) -> None:
    """
    One iteration of the crab-cups game
    """
    # Get the current node
    current_node = self._current_node
    # Get the next 3 nodes
    next_node = current_node.next
    next_next_node = next_node.next
    next_next_next_node = next_next_node.next
    # The next 3 values and 0 can't be the destination
    bad_nums = {
        0,
        next_node.value,
        next_next_node.value,
        next_next_next_node.value,
    }
    # Look for destination, from current value, `O(1)`
    dest_value = current_node.value
    while True:
        dest_value -= 1
        if not dest_value:
            dest_value = self._max
        if dest_value not in bad_nums:
            break
    # Get destination node, `O(1)` average
    dest_node = self._value_node_map[dest_value]
    # Remove the 3 elements, `O(1)`
    current_node.next = next_next_next_node.next
    # Add the 3 elements after destination, `O(1)`
    next_next_next_node.next = dest_node.next
    dest_node.next = next_node
    # Go to the next node, preparing for the next loop
    self._current_node = current_node.next
```
