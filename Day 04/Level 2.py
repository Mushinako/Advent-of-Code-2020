#!/usr/bin/env python3
"""
Solution to part 2
"""
import re
from pathlib import Path
from typing import Callable

from aoc_io.aoc_io import DATA_FILENAME, submit_output

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

# Read input
with INPUT_FILE_PATH.open("r") as input_fp:
    people = input_fp.read().replace("\n", " ").split("  ")

REQUIRED: dict[str, Callable[[str], bool]] = {
    "byr": (lambda x: int(x) in range(1920, 2002 + 1)),
    "iyr": (lambda x: int(x) in range(2010, 2020 + 1)),
    "eyr": (lambda x: int(x) in range(2020, 2030 + 1)),
    "hgt": (
        lambda x: int(x[:-2])
        in (range(150, 193 + 1) if x[-2:] == "cm" else range(59, 76 + 1))
    ),
    "hcl": (lambda x: bool(re.fullmatch(r"^#[0-9a-f]{6}$", x))),
    "ecl": (lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}),
    "pid": (lambda x: bool(re.fullmatch(r"^\d{9}$", x))),
}

count = 0

for person in people:
    passport = {}
    for entry in person.split():
        key, value = entry.split(":")
        passport[key] = value
    for key, verifunc in REQUIRED.items():
        value = passport.get(key)
        if value is None:
            break
        if not verifunc(value):
            break
    else:
        count += 1

print(count)
print(submit_output(2020, 4, 2, count))