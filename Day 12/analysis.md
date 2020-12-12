# [Day 12: Rain Risk](https://adventofcode.com/2020/day/12)

## Part 1

Maybe it's because that I'm a math person, but the first thing that comes to my
mind about 2D rotations is complex numbers, which provides nice
[rotation](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-ac-analysis/v/ee-complex-rotation)
methods.

```py
ship = 0.0 + 0.0j
direction = 1.0 + 0.0j

for action, num in moves:
    if action == "N":
        ship += num * (0.0 + 1.0j)
    elif action == "S":
        ship -= num * (0.0 + 1.0j)
    elif action == "E":
        ship += num * (1.0 + 0.0j)
    elif action == "W":
        ship -= num * (1.0 + 0.0j)
    elif action == "F":
        ship += num * direction
    elif action == "L":
        direction *= cmath.exp(math.radians(num) * 1.0j)
    elif action == "R":
        direction /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(action)

result = round(abs(ship.real)) + round(abs(ship.imag))
```

The `1.0 + 0.0j` is the "unit vector" pointing east (positive x direction).

## Part 2

One nice thing about the complex number approach is that it actually provides a
very nice solution for part 2 as well. The change in the code is minimal. See
if you can spot it.

```py
ship = 0.0 + 0.0j
direction = 10.0 + 1.0j

for action, num in moves:
    if action == "N":
        direction += num * (0.0 + 1.0j)
    elif action == "S":
        direction -= num * (0.0 + 1.0j)
    elif action == "E":
        direction += num * (1.0 + 0.0j)
    elif action == "W":
        direction -= num * (1.0 + 0.0j)
    elif action == "F":
        ship += num * direction
    elif action == "L":
        direction *= cmath.exp(math.radians(num) * 1.0j)
    elif action == "R":
        direction /= cmath.exp(math.radians(num) * 1.0j)
    else:
        raise ValueError(action)

result = round(abs(ship.real)) + round(abs(ship.imag))
```

The actual changes is to replace the `d` as the initial waypoint position and
changing the cardinal movements (`NSEW`) to affect waypoint instead of the ship.
