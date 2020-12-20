# [Day 10: Adapter Array](https://adventofcode.com/2020/day/10)

## Part 1

More or less a brute-force this time as well. The numbers are first sorted
because that'll be the order that they're chained. Don't forget to add the outlet
(`0`) and your device, which automatically has a difference of 3.

```py
with INPUT_FILE_PATH.open("r") as input_fp:
    jolts = [0] + [int(line.strip()) for line in input_fp]

jolts.sort()

jolt_1 = 0
jolt_3 = 1

for i, jolt in enumerate(jolts[:-1]):
    next_jolt = jolts[i + 1]
    diff = next_jolt - jolt
    if diff == 1:
        jolt_1 += 1
    elif diff == 3:
        jolt_3 += 1
    elif diff >= 4:
        break
```

P.S., there're definitely cooler ways (one-liners). I just personally find this
more readable.

## Part 2

All hail `functools.cache` (Py 3.9) or `functools.lru_cache` (Py 3.2-3.8)! That
was effectively the optimization for my recursive algorithm.

```py
@cache
def count_ways(jolts: tuple[int, ...]) -> int:
    if len(jolts) == 0:
        return 0
    if len(jolts) == 1:
        return 1
    if jolts[1] - jolts[0] > 3:
        return 0
    cumulative = 0
    cumulative += count_ways(jolts[1:])
    if len(jolts) == 2 or jolts[2] - jolts[0] > 3:
        return cumulative
    cumulative += count_ways(jolts[2:])
    if len(jolts) == 3 or jolts[3] - jolts[0] > 3:
        return cumulative
    return cumulative + count_ways(jolts[3:])
```
