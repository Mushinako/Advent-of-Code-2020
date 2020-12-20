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
    "byr": (lambda x: 1920 <= int(x) <= 2002),
    "iyr": (lambda x: 2010 <= int(x) <= 2020),
    "eyr": (lambda x: 2020 <= int(x) <= 2030),
    "hgt": (
        lambda x: (
            150 <= int(x[:-2]) <= 193 if x[-2:] == "cm" else 59 <= int(x[:-2]) <= 76
        )
    ),
    "hcl": (lambda x: bool(re.fullmatch(r"^#[0-9a-f]{6}$", x))),
    "ecl": (lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}),
    "pid": (lambda x: len(x) == 9 and x.isdigit()),
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