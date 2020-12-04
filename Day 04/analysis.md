# [Day 04: Passport Processing](https://adventofcode.com/2020/day/4)

## Part 1

The difficult part seems to be file parsing. While you can brute-force the parsing,
reading file line-by-line, and keep track of when each person's data ends, I chose
to look for double newline characters which separates data for each person. I
replaced newlines (`\n`) with spaces, and checked for double spaces.

```py
people = input_fp.read().replace("\n", " ").split("  ")
```

After getting each person's data, I can split by space and then by `:` to get the
keys. The last thing to do is to check whether all the required keys are present.

```py
keys = {entry.split(":")[0] for entry in person.split()}
if keys >= REQUIRED:
    count += 1
```

## Part 2

The second part is similar. The difference is that we need some checking on each
piece of data. The code is a little different, given that value check is added.

Firstly, all the verification functions are added:

```py
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
```

All the verification functions receive a `str` (the value of each entry) and return
a bool (whether the value is valid).

* **byr**, **iyr**, **eyr**: Converts the value to `int`, and checks whether it's
  in range.
* **hgt**: Converts everything except the last 2 characters into number, and checks
  whether it's in range. The range is dependent on the last 2 characters.
* **hcl**, **pid**: Regex is probably the best solution here.
* **ecl**: Nice `O(1)` membership check in `set`.

All the checks can be run in a loop:

```py
for key, verifunc in REQUIRED.items():
    value = passport.get(key)
    if value is None:
        break
    if not verifunc(value):
        break
else:
    count += 1
```

This solution utilizes `for-else` to check whether a condition is not satisfied.
The counter is incremented only if the loop is not broken.
