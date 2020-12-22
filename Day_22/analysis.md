# [Day 22: Crab Combat](https://adventofcode.com/2020/day/22)

## Part 1

Another implementation problem it seems. Basically implement the rules and
described and you're good to go!

```py
def level1() -> int:
    """
    Level 1 solution

    Returns:
        (int): Solution to the problem
    """
    player1, player2 = read_input(_INPUT_FILE_PATH)
    while player1 and player2:
        p1 = player1.popleft()
        p2 = player2.popleft()
        if p1 > p2:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)
    total = list(player1)[::-1] + list(player2)[::-1]
    return sum((i + 1) * n for i, n in enumerate(total))
```

## Part 2

Also implementation, and the problem nicely told us that recursion is involved!

```py
def _game(player1: deque[int], player2: deque[int]) -> tuple[bool, list[int]]:
    """"""
    player1_prevs: set[frozenset[int]] = set()
    player2_prevs: set[frozenset[int]] = set()
    while True:
        if not player1:
            return False, list(player2)[::-1]
        elif not player2:
            return True, list(player1)[::-1]
        if (p1f := frozenset(player1)) in player1_prevs or (
            p2f := frozenset(player2)
        ) in player2_prevs:
            return True, list(player1)[::-1]
        player1_prevs.add(p1f)
        player2_prevs.add(p2f)
        p1 = player1.popleft()
        p2 = player2.popleft()
        if p1 <= len(player1) and p2 <= len(player2):
            winner, _ = _game(deque(list(player1)[:p1]), deque(list(player2)[:p2]))
            if winner:
                player1.append(p1)
                player1.append(p2)
            else:
                player2.append(p2)
                player2.append(p1)
        else:
            if p1 > p2:
                player1.append(p1)
                player1.append(p2)
            else:
                player2.append(p2)
                player2.append(p1)
```
