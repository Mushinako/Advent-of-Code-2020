# [Day 15: Rambunctious Recitation](https://adventofcode.com/2020/day/15)

## Part 1

Brute force!

```py
while len(nums) < 2020:
    consideration = nums[-1]
    if nums.count(consideration) == 1:
        nums.append(0)
    else:
        gap = nums[::-1][1:].index(consideration) + 1
        nums.append(gap)

result = nums[-1]
```

## Part 2

The problem with part 1's solution is that `list.count` and `list.index` are
`O(n)`, which is *very* slow for 30 million iterations. For that, we need
something that is average `O(1)`: `dict` access.

```py
nums_dict = {num: i + 1 for i, num in enumerate(nums[:-1])}
consideration = nums[-1]

for i in range(len(nums), 30_000_000):
    if consideration in nums_dict:
        new_last_num = i - nums_dict[consideration]
    else:
        new_last_num = 0
    nums_dict[consideration] = i
    consideration = new_last_num

result = consideration
```
