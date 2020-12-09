# [Day 09: Encoding Error](https://adventofcode.com/2020/day/9)

## Part 1

Another problem that asks for sums to a specific number. This is resolved
here by brute force. Given a lot of `popleft` and `append`, I chose
`collections.deque` to take advantage of the `O(1)`. The basic method is
same as that of Day 1.

## Part 2

Another brute-force. Start with each number and keep adding until the sum is
greater than or equal to the target (part 1 solution). If the sum is too
large, try starting from the next number.
