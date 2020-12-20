# [Day 08: Handheld Halting](https://adventofcode.com/2020/day/8)

## Part 1

This is a rather straightforward logic implementation. The travered code indices
are saved in a set and checked whether some instruction had been reached before.

```py
ids = set()
acc = 0
pointer = 0

while True:
    if pointer in ids:
        break
    ids.add(pointer)
    command, param = code[pointer]
    if command == "acc":
        acc += param
        pointer += 1
    elif command == "jmp":
        pointer += param
    elif command == "nop":
        pointer += 1
    else:
        raise ValueError(f"{acc} {pointer}")
```

## Part 2

I took a brute-force approach to the 2nd part, iterating through all the possible
mutations and try them. `O(n^2)` looping go brrrrr.

```py
for i in range(len(code)):
    if code[i][0] == "jmp":
        replacement = "nop"
    elif code[i][0] == "nop":
        replacement = "jmp"
    else:
        continue

    new_code = [list(a) for a in code]
    new_code[i][0] = replacement

    ids = set()
    acc = 0
    pointer = 0

    while True:
        if pointer >= len(new_code):
            return acc
        if pointer in ids:
            break
        ids.add(pointer)
        command, param = new_code[pointer]
        if command == "acc":
            acc += param
            pointer += 1
        elif command == "jmp":
            pointer += param
        elif command == "nop":
            pointer += 1
        else:
            raise ValueError(f"{acc} {pointer}")
```
