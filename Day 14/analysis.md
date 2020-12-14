# [Day 14: Docking Data](https://adventofcode.com/2020/day/14)

## Part 1

The first part is resolved with brute-force. Also, just learnt about `str.zfill`!

```py
mask = ""

for action, value in instructions:
    if action == "mask":
        mask = value
    else:
        index = int(action[4:-1])
        binary = bin(int(value))[2:].zfill(36)
        new_binary = ""
        for i in range(36):
            if mask[i] == "X":
                new_binary += binary[i]
            else:
                new_binary += mask[i]
        memory[index] = int(new_binary, 2)

result = sum(memory.values())
```

## Part 2

I chose to keep track of the digits where quantum stuff happens (`floatings`),
then add the floating stuffs back in in a double for-loop.

```py
mask = ""

for action, value in instructions:
    if action == "mask":
        mask = value
    else:
        index = int(action[4:-1])
        value = int(value)
        binary = bin(index)[2:].zfill(36)
        new_binary = ""
        floatings = []
        for i in range(36):
            if mask[i] == "0":
                new_binary += binary[i]
            elif mask[i] == "1":
                new_binary += "1"
            else:
                new_binary += "0"
                floatings.append(35 - i)
        base_num = int(new_binary, 2)
        for i in range(2 ** len(floatings)):
            new_num = base_num
            for j, power in enumerate(floatings):
                i, rem = divmod(i, 2)
                if rem:
                    new_num += 2 ** power
            memory[new_num] = value

result = sum(memory.values())
```
