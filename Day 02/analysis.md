# [Day 02: Password Philosophy](https://adventofcode.com/2020/day/2)

## Part 1

The most annoying part here is parsing the input, yet reasonably straightforward.
Due to the amount of text processing, I decided to read each line and process them
on the spot (instead of my usual way, which is to put it in a `list`). The main
pattern of each line is `{lower}-{upper} {letter}: {password}`, and there're many
ways to parse the input, the easiest to read is probably regex `re`.

```py
pattern = re.compile(r"^(?P<lower>)-(?P<upper>) (?P<letter>): (?P<password>)$")
match = pattern.match(line)
lower = int(match["lower"])
upper = int(match["upper"])
letter = match["letter"]
password = match["password"]
```

I, however, am lazy, so I chose the less readable way, which is to split the
string manually.

```py
counts, letter, password = line.split()
lower, upper = [int(n) for n in counts.split("-")]
letter = letter[0]
```

Once the string is parsed, the check is basically to get the number of letter
occurrences, and see if it's in the between `lower` and `upper`.

```py
password.count(letter) in range(lower, upper + 1)
```

## Part 2

The input parsing part is basically the same. The first thing to notice is that the
inputs under the new rule is 1-based indices, so subtrace 1 from them to get
0-based indices. The check is also different. Now it checks whether 1 and only 1 of
the 2 letters at the 2 indices is the required letter. Seems like XOR `^` is made
for this situation.

```py
(password[lower] == letter) ^ (password[upper] == letter)
```
