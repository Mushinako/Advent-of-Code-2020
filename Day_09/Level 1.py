#!/usr/bin/env python3
"""
Solution to part 1
"""
from collections import deque
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    nums = [int(line.strip()) for line in input_fp]

queue = deque(nums[:25])
left = deque(nums[25:])

while True:
    queue_set = set(queue)
    next_num = left.popleft()
    for num in queue:
        remainder = next_num - num
        if remainder in queue_set - {num}:
            break
    else:
        break
    queue.popleft()
    queue.append(next_num)


print(next_num)
print(submit_output(2020, 9, 1, next_num))