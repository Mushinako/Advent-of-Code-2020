#!/usr/bin/env python3
"""
Solution to part 2
"""
# pyright: reportGeneralTypeIssues=false
from math import lcm
from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    input_fp.readline()
    line = input_fp.readline().strip().split(",")
    length = len(line)
    buses = [(t, int(num)) for t, num in enumerate(line) if num != "x"]


def crt(mods_rems: list[tuple[int, int]]) -> int:
    """
    Chinese Remainder Theorem

    Args:
        mods_rems (list[tuple[int, int]]): List of [modulus, remainder] pairs

    Returns:
        (int): The smallest positive number that satisfies all the
               modulus-remainder constraints.
    """
    sum_ = 0
    # Least common multiple of all moduli
    prod = lcm(*(m for m, _ in mods_rems))
    # Iterate through each modulus, find multiple of all other moduli and
    #   multiply it by it's multiplicative inverse
    for mod, rem in mods_rems:
        # This is the lcm of all other moduli because the moduli are assumed to
        #   be coprime with one another
        prod_left = prod // mod
        # Add remainder * lcm(other moduli) * its multiplicative inverse
        sum_ += rem * prod_left * mul_inv(prod_left, mod)
    return sum_ % prod


def mul_inv(n: int, m: int) -> int:
    """
    Calculate n^(-1) mod m, or equivalently, find y for n*y + m*x = 1 via the
      Extended Euclidean Algorithm

    Args:
        n (int): The number to be inverted
        m (int): The modulus

    Returns:
        (int): The multiplicative inverse
    """
    # Mod 1, not very useful
    if m == 1:
        return 1
    # Keep a record of the original modulus
    tmp = m
    # Initiate x, y as 0, 1
    x = 0
    y = 1
    while n > 1:
        quotient = n // m
        n, m = m, n % m
        x, y = y - quotient * x, x
    # Make `y` positive, if it isn't
    if y < 0:
        y += tmp
    return y


mods_rems = [(num, num - t % num) for t, num in buses]
result = crt(mods_rems)

print(result)
print(submit_output(2020, 13, 2, result))