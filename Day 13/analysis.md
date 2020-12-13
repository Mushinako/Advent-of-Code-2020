# [Day 13: Shuttle Search](https://adventofcode.com/2020/day/13)

## Part 1

The first part is reasonably straightforward. Calculate the time for each bus
to arrive, and find the minimum.

```py
schedules = [(b - ts % b, b) for b in buses]

min_ = min(schedules)
result = min_[0] * min_[1]
```

## Part 2

At first I thought the problem can be brute-forced, given that the numbers seemed
small. Nevertheless, I still decided to go for
[Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem).

```py
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
```

### Chinese Remainder Theorem

(Estimated read time 14 minutes; estimated time to understand 2 hours)

#### Intro

The Chinese Remainder Theorem is used to calculate a number that satisfies some
restraints when modded by some numbers. There was a story of an ancient Chinese
general named [Han Xin](https://en.wikipedia.org/wiki/Han_Xin), who led 1500
solders into a battle. After the battle, he knew `400-500` soldiers have died,
but not sure how many exactly. He ordered the solders to stand in rows.

* The soldiers stood into 3 rows. 2 people were left at the end.
* The soldiers stood into 5 rows. 4 people were left at the end.
* The soldiers stood into 7 rows. 3 people were left at the end.

In mathematically terms:

```text
x ≡ 2 (mod 3)
x ≡ 4 (mod 5)
x ≡ 3 (mod 7)
```

Given that the number of soldiers is `1000-1100`, only `1004` satisfies the
conditions above.

#### `mod`?

In short, the `mod` gets the remainder when divided. `75 ≡ 5 (mod 7)` means if
you divide `75` by `7`, the remainder is `5`. If you know Python's modulo
operator `%`, then the above equation is `75 % 7 == 5`. In this walkthrough, I'll
mainly write the mod stuff in the first way, which is the math way. There're some
occurrences where I use the Pythonic way `%` and `//`, which is due to difficulty
in writing math using Markdown.

### The Smart Way

While one can try all numbers between `1000` and `1100`, it's quite tedious,
especially when the range of possible answers is very large. It is said that
when asked about the calculation, Han said that he first calculated
`70 * 2 + 21 * 4 + 15 * 3 = 269`; he then kept adding `105` until the number is
`1000-1100`, and `1004` is the only answer.

### Why Does `70 * 2 + 21 * 4 + 15 * 3` Adding Multiple `105`s Work?

While the `2`, `4`, and `3` in the above formula makes sense, where does the
other numbers `70`, `21`, `15`, and `105` come from?

Let's first examine what's special about these numbers, by modding them against
`3`, `5`, and `7`.

```text
 70 ≡ 1 (mod 3);  70 ≡ 0 (mod 5);  70 ≡ 0 (mod 7) [multiplied by remainder of 3]
 21 ≡ 0 (mod 3);  21 ≡ 1 (mod 5);  21 ≡ 0 (mod 7) [multiplied by remainder of 5]
 15 ≡ 0 (mod 3);  15 ≡ 0 (mod 5);  15 ≡ 1 (mod 7) [multiplied by remainder of 7]
105 ≡ 0 (mod 3); 105 ≡ 0 (mod 5); 105 ≡ 0 (mod 7)
```

Notice that `70` is multiplied by the remainder when counting by `3`
as it's `1` when modded by `3` and `0` otherwise. Same for `21` and `15`: they
mod to `1` for the number with whose remainder it is multiplied, and `0`
otherwise.

#### Addition and Multiplication in Modulo

The interesting thing about modulo is that you can add or multiply both sides by
a number and the equality (congruency?) still holds. For example, comparing `31`
and `31 + 31 = 31 * 2 = 62`:

```text
 31 ≡ 1 (mod 3); 31 + 31 = 31 * 2 = 62 ≡ 2 = 1 * 2 = 1 + 1 (mod 3)
 31 ≡ 1 (mod 5); 31 + 31 = 31 * 2 = 62 ≡ 2 = 1 * 2 = 1 + 1 (mod 5)
 31 ≡ 3 (mod 7); 31 + 31 = 31 * 2 = 62 ≡ 6 = 3 * 2 = 3 + 3 (mod 7)
```

So in general, if `n ≡ a (mod m)`, then `n + b ≡ a + b (mod m)` and
`n * b ≡ a * b (mod m)`.

Now let's check how `70 * 2 + 21 * 4 + 15 * 3` mods `3`, `5`, and `7`:

```text
269 = 70 * 2 + 21 * 4 + 15 * 3 ≡ 1 * 2 + 0 * 4 + 0 * 3 = 2 (mod 3)
269 = 70 * 2 + 21 * 4 + 15 * 3 ≡ 0 * 2 + 1 * 4 + 0 * 3 = 4 (mod 5)
269 = 70 * 2 + 21 * 4 + 15 * 3 ≡ 0 * 2 + 0 * 4 + 1 * 3 = 3 (mod 7)
```

Hey! `70 * 2 + 21 * 4 + 15 * 3` satisfies our constraints!

Now we can keep adding or subtracting `105`, which is `0` when modded by all 3
numbers:

```text
269 + 105 * n ≡ 2 + 0 * n = 2 (mod 3)
269 + 105 * n ≡ 4 + 0 * n = 4 (mod 5)
269 + 105 * n ≡ 3 + 0 * n = 3 (mod 7)
```

### Why `70`, `21`, `15`, and `105`?

That's all nice and good, but *where* did I get those numbers? So far I just
pulled them out of thin air and showed that they're special, but I haven't
discussed how to find them.

The `105` is probably the easiest to find. It needs to have a remainder of `0`
when divided by all the moduli. In other words, it has to be a multiple of all
the moduli. The
[least common multiple](https://en.wikipedia.org/wiki/Least_common_multiple) is
a good choice, and in Python 3.9+ we have `math.lcm` to calculate that.

Finding `70`, `21`, and `15` are much trickier. These numbers have to have a
remainder of `1` when divided by one of the moduli, and `0` for all other moduli.

Finding a number that has a remainder of `0` for other moduli is rather simple.
Just take the least common multiple of other numbers. The issue, however, is to
find a number that has a remainder of exactly `1`.

Let's say that I want to find the number for modulus `3`. Firstly, the number
has to divide `5` and `7`. So let's start with their least common multiple: `35`.
Note that for any integer `y`, `35 * y` also divides both `3` and `5`. So can we
find an `y` that makes `35 * y` has a remainder of `1` when divided by `3`?

```text
35 * y ≡ 1 (mod 3)
```

Fun fact: the `y` in this case is called the
[modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse),
because `35` and `y` multiply to `1` in the modded space.

Thinking about the definition of modulo/remainder, the above equation means that
there's some number `x` such that:

```text
35 * y + 3 * x = 1
```

`x` in this case is actually the negative quotient, which is the integer part you
get when you do the division `-(35 // 3)`. But how do we solve for `y`?

### Finding `70`, `21`, and `15`

The way to solve `35 * y + 3 * x = 1` is the
[Extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm).

Before we talk about how extended Euclidean algorithm works, we have to take a
detour to (non-extended)
[Euclidean algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm).

#### Euclidean algorithm

The Euclidean algorithm is an efficient way to find the
[greatest common divisor](https://en.wikipedia.org/wiki/Greatest_common_divisor)
of two integers. The basis of this algorithm is simple: for integers `a` and `b`
where `a > b`, `gcd(a, b) = gcd(b, a % b)`.

This property may not be immediately obvious, and my walkthrough below requires
some math. Feel free to take this algorithm as granted and skip to the
[next section](#euclidean-algorithm-procedure).

##### `gcd(a, b) = gcd(b, a % b)`

For those who are still here, hi! Let's say the the greatest common divisor of
`a` and `b` is `d`.

```text
a = d * m   (1)
b = d * n   (2)
```

Given that `d` is the greatest common divisor, `m` and `n` have to be coprime to
each other, i.e., `gcd(m, n) = 1`.

Then what would `a % b` be? Let's try dividing `a` by `b`:

```text
a = q * b + r   (3)
```

For you Python nerds:

```py
q, r = divmod(a, b)
```

The `r` is the `a % b` we're interested in and therefore would like to solve for,
which we can do thusly from *Eq. (3)*:

```text
r = a - q * b
```

We can substitue `a` and `b` above with *Eq. (1), (2)*:

```text
r = (d * m) - q * (d * n) = d * (m - q * n)
```

Putting `b` and `r` (`a % b`) side-by-side:

```text
b = d * n
r = d * (m - q * n)
```

It's clear to see that `b` and `r` share a common factor of `d`, just like `a`
and `b`.

Some of you may have a question: what if `n` and `m - q * n` has extra common
factors? In that case, `gcd(b, a % b) > gcd(a, b)`. Fortunately, that's not possible, and here's why:

Say `n` and `m - q * n` shares extra common factor `e > 1`. Then:

```text
        n = e * i   (4)
m - q * n = e * j   (5)
```

We're interest in solving for `m`. Therefore, rearrange *Eq. (5)*:

```text
m = q * n + e * j   (6)
```

Substituting `n` in *Eq. (6)* with *Eq. (4)* gives:

```text
m = q * (e * i) + e * j = e * (q * i + j)
```

In that case, `m` will also share the factor `e`, but that's not possible given
`m` and `n` are coprime.

With all above, we can confidently say that `gcd(a, b) = gcd(b, a % b)`.

##### Euclidean algorithm procedure

Welcome back if you skipped the previous section! Now we're going to talk about
How Euclidean algorithm works, which is basically repetitively applying the
formula above: `gcd(a, b) = gcd(b, a % b)`.

Let's say that I want to calculate `gcd(35, 3)`:

```text
gcd(35, 3) = gcd(3, 35 % 3)
           = gcd(3, 2)      = gcd(2, 3 % 2)
                            = gcd(2, 1)     = gcd(1, 2 % 1)
                                            = gcd(1, 0)     = 1
```

The algorithm stops when the second term becomes `0`. The solution is then the
first term, which is `1` here.

#### Extended Euclidean Algorithm

The Euclidean Algorithm gives a way to solve for `x` and `y` in
`m * x + n * y = gcd(m, n)`, where `m` and `n` are constants. More math incoming!
This math should be easier, but if you want to skip,
[feel free](#extended-euclidean-algorithm-procedure)!

##### More Math

Let's go back to how we calculated `gcd(35, 3)` and walk backwards.

* `gcd(1, 0)` is where we got the solution `1`. That the final step, not very
  interesting.
* `gcd(2, 1)` is the second-to-last step. The `1` is the same `1` as that in the
  final step, so this is also not really interesting.
* `gcd(3, 2)` is much more interesting. We got the `1` via `3 % 2`. By the
  definition of remainders:

  ```text
  1 = 3 % 2 = 3 - (3 // 2) * 2   (7)
  ```

  The remainder is, essentially, the dividend minus quotient times divisor.
* `gcd(35, 3)` is one level higher, giving a similar formula:

  ```text
  2 = 35 % 3 = 35 - (35 // 3) * 3   (8)
  ```

  Substituting `2` in *Eq. (7)* with *Eq. (8)* gives:

  ```text
  1 = 3 - (3 // (35 - (35 // 3) * 3)) * (35 - (35 // 3) * 3)
    = 3 - (3 // (35 - (35 // 3) * 3)) * 35 + (3 // (35 - (35 // 3) * 3)) * (35 // 3) * 3
    = 3 * (1 + (3 // (35 - (35 // 3) * 3)) * (35 // 3)) + 35 * (-(3 // (35 - (35 // 3) * 3)))
  ```

  Hey we got it in the form of `1 = 3 * x + 35 * y` (although the `x` and `y`,
  but all the numbers are either `35` and `3` as well!) are quite messy. Don't
  worry, we can simplify it:

  ```text
  1 = 3 * (1 + (3 // (35 - (35 // 3) * 3)) * (35 // 3)) + 35 * (-(3 // (35 - (35 // 3) * 3)))
    = 3 * (1 + (3 // 2) * 11) + 35 * (-(3 // 2))
    = 3 * (12) + 35 * (-1)
  ```

#### Extended Euclidean Algorithm Procedure

Summarizing the essential math part of calculations above:

```text
1 =  3 - ( 3 // 2) * 2
2 = 35 - (35 // 3) * 3
^    ^       ^       ^
n%m n(y) quotient   m(x)
```

In essence, the algorithm calls for a loop with thesee statements:

```py
quotient = n // m
n, m = m, n % m
x, y = y - quotient * x, x
```

A small "hack" is to initiate `x` as `0` and `y` as `1`. This will increase the
number of loops run by 2, but it frees you from having to manually calculate the
starting numbers.

```py
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
    # Main Euclidean algorithm part
    while n > 1:
        quotient = n // m
        n, m = m, n % m
        x, y = y - quotient * x, x
    # Make `y` positive, if it isn't
    if y < 0:
        y += tmp
    return y
```

### Putting It All Together

So to recap, to find a number that satisfies a list of modulus-remainder
constraints via the Chinese remainder theorem:

1. For each modulus, find the **least common multiple** of **all other moduli**,
   and multiply it by its **multiplicative inverse** with regard to the current
   modulus so that the product has a remainder of `1` to the modulus.
2. Sum all the numbers from *Step 1*.
3. Add/subtract the **least common multiple** of **all moduli**.

```py
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
```

Or you can use
[`sympy.ntheory.modular.crt`](https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.modular.crt)
if you don't want to implement this yourself.

### Endnote

The choice of the moduli are not exactly arbiturary or random. The moduli have to
be [coprime](https://en.wikipedia.org/wiki/Coprime_integers) with one another. In
other words, for any pair of moduli chose `a`, `b`, `gcd(a, b)` has to be `1`.
It's usually the easiest to choose different prime numbers or powers of different
prime numbers as moduli, as they're guaranteed to be coprime to one another.
