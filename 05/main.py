import fileinput
from collections import defaultdict


def parse():
    reading_rules = True
    rules = defaultdict(list)
    updates = []
    for line in fileinput.input():
        if line == "\n":
            reading_rules = False
            continue
        if reading_rules:
            a, b = line.strip().split("|")
            rules[int(a)].append(int(b))
        else:
            updates.append([int(a) for a in line.strip().split(",")])
    return rules, updates


def is_in_order(update, rules):
    index_by_value = {v: i for i, v in enumerate(update)}
    for v in update:
        if any(
            index_by_value[after] < index_by_value[v]
            for after in rules[v]
            if after in index_by_value
        ):
            return False
    return True


def filter(rules, updates):
    in_order = [update for update in updates if is_in_order(update, rules)]
    return sum([update[len(update) // 2] for update in in_order])


def fix(rules, updates):
    not_in_order = [update for update in updates if not is_in_order(update, rules)]
    ordered = [topsort(update, rules) for update in not_in_order]
    return sum([o[len(o) // 2] for o in ordered])


def topsort(update, rules):
    seen = set()
    ordered = []

    def search(v):
        if v in seen:
            return
        for w in rules[v]:
            if w in update:
                search(w)
        seen.add(v)
        ordered.append(v)
        return

    for v in update:
        search(v)
    return list(reversed(ordered))


def main():
    rules, updates = parse()
    print(f"Part 1: {filter(rules, updates)}")
    print(f"Part 2: {fix(rules, updates)}")


if __name__ == "__main__":
    main()
