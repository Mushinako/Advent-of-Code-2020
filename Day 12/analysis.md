# [Day 12: Rain Risk](https://adventofcode.com/2020/day/12)

## Part 1

Maybe it's because that I'm a math person, but the first thing that comes to my
mind about 2D rotations is complex numbers, which provides nice
[rotation](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-ac-analysis/v/ee-complex-rotation)
methods.

```py
ship = 0.0 + 0.0j
d = 1.0 + 0.0j

for direction, num in moves:
    if direction == "N":
        ship += num * (0.0 + 1.0j)
    elif direction == "S":
        ship -= num * (0.0 + 1.0j)
    elif direction == "E":
        ship += num * (1.0 + 0.0j)
    elif direction == "W":
        ship -= num * (1.0 + 0.0j)
    elif direction == "F":
        ship += num * d
    elif direction == "L":
        d *= cmath.exp(math.radians(num) * 1.0j)
    elif direction == "R":
        d /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(direction)

result = round(abs(ship.real)) + round(abs(ship.imag))
```

The `1.0 + 0.0j` is the "unit vector" pointing east (positive x direction).

## Part 2

One nice thing about the complex number approach is that it actually provides a
very nice solution for part 2 as well. The change in the code is minimal. See
if you can spot it.

```py
ship = 0.0 + 0.0j
d = 10.0 + 1.0j

for direction, num in moves:
    if direction == "N":
        d += num * (0.0 + 1.0j)
    elif direction == "S":
        d -= num * (0.0 + 1.0j)
    elif direction == "E":
        d += num * (1.0 + 0.0j)
    elif direction == "W":
        d -= num * (1.0 + 0.0j)
    elif direction == "F":
        ship += num * d
    elif direction == "L":
        d *= cmath.exp(math.radians(num) * 1.0j)
    elif direction == "R":
        d /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(direction)

result = round(abs(ship.real)) + round(abs(ship.imag))
```

The actual changes is to replace the `d` as the initial waypoint position and
changing the cardinal movements (`NSEW`) to affect waypoint instead of the ship.
