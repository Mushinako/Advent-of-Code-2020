# [Day 16: Ticket Translation](https://adventofcode.com/2020/day/16)

Sidenote: I'm currently transitioning to the new code structure. Hopefully the
inconsistency is not bothering.

## Part 1

Brute force works well, especially because of `O(1)` set membership check.
(Although space efficiency is nonexistent)

```py
rule_nums = set()
while (line := fp.readline().strip()) :
    _, ranges_str = line.split(": ")
    for r in ranges_str.split(" or "):
        start, end = r.split("-")
        rule_nums |= set(range(int(start), int(end) + 1))

rule_nums, nearby_nums = _read_input()
return sum(n for n in nearby_nums if n not in rule_nums)
```

An alternative that's much more space-efficient but potentially a little slower
is just check `start <= value <= end` instead of
`value in set(range(start, end+1))`.

## Part 2

While my part 2 solution may seen long and discouraging, the idea is relatively
simple, and it's just that I tried to make everything more verbose than probably
necessary.

The general idea is to check each field and column. If a field has only 1 column
that satisfy it or a column has only one field that it satisfies, then we know
that column corresponds to that field. Remove the column and the field from the
pool and repeat the process.

The given test cases are actually very cleverly constructed, and you'll find that
in each loop, exactly 1 field has only 1 column and only 1 column has 1 field.
Given that there're 20 fields and columns, the whole process takes 10 loops (each
field has a matching column and each column has a matching field), which is much
faster than my original attempt to brute-force it, which would take
`20! = 2,432,902,008,176,640,000` loops.

After the inputs are read, the connections are first initalized:

```py
# Or a double for-loop
for rule, ticket_col in product(rules.values(), ticket_cols.values()):
    rule.add_valid(ticket_col)
```

Each loop removes 2 field-column pairs

```py
class _RuleColumnMap:
    def add_singles(self, rules: dict[str, _Rule], cols: dict[int, _Column]) -> bool:
        """
        Add rules with only 1 matching column and columns with only 1 matching
          rule

        Args:
            rules (dict[str, _Rule])  : A collection of rules to be checked
            cols  (dict[int, _Column]): A collection of columns to be checked

        Returns:
            (bool): Whether any changes are made
        """
        rules_added = self._add_single_rules(rules, cols)
        cols_added = self._add_single_cols(cols, rules)
        return rules_added or cols_added

    def _add_single_rules(
        self, rules: dict[str, _Rule], cols: dict[int, _Column]
    ) -> bool:
        """
        Add rules with only 1 matching column

        Args:
            rules (dict[str, _Rule])  : A collection of rules to be checked
            cols  (dict[int, _Column]): A collection of columns

        Returns:
            (bool): Whether any changes are made
        """
        added_rules: set[_Rule] = set()
        added_cols: set[_Column] = set()
        for rule in rules.values():
            if rule.valid_col_count > 1:
                continue
            if not rule.valid_col_count:
                raise ValueError(f"{rule.name} has no matching columns")
            col = rule.valid_cols.pop()
            self.map_[rule.name] = col.id_
            added_rules.add(rule)
            added_cols.add(col)
        for rule in added_rules:
            del rules[rule.name]
        for rule in rules.values():
            rule.valid_cols -= added_cols
        for col in added_cols:
            del cols[col.id_]
        for col in cols.values():
            col.satisfied_rules -= added_rules
        return bool(added_rules)

    def _add_single_cols(
        self, cols: dict[int, _Column], rules: dict[str, _Rule]
    ) -> bool:
        """
        Add columns with only 1 matching rule

        Args:
            cols  (dict[int, _Column]): A collection of columns to be checked
            rules (dict[str, _Rule])  : A collection of rules

        Returns:
            (bool): Whether any changes are made
        """
        added_cols: set[_Column] = set()
        added_rules: set[_Rule] = set()
        for col in cols.values():
            if col.satisfied_rule_count > 1:
                continue
            if not col.satisfied_rule_count:
                raise ValueError(f"{col.id_} has no matching rules")
            rule = col.satisfied_rules.pop()
            self.map_[rule.name] = col.id_
            added_cols.add(col)
            added_rules.add(rule)
        for col in added_cols:
            del cols[col.id_]
        for col in cols.values():
            col.satisfied_rules -= added_rules
        for rule in added_rules:
            del rules[rule.name]
        for rule in rules.values():
            rule.valid_cols -= added_cols
        return bool(added_cols)

while rule_column_map.add_singles(rules, cols):
    pass
```

After 10 loops the mapping is got, and then we can get the product:

```py
indices = (
    i
    for rule_name, i in rule_column_map.map_.items()
    if rule_name.startswith("departure")
)
return prod(your_ticket[i] for i in indices)
```
