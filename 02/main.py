import fileinput
from itertools import pairwise


def parse():
    reports = []
    for line in fileinput.input():
        reports.append([int(i) for i in line.split()])
    return reports


def is_safe(report):
    descending = report[0] > report[1]
    for a, b in pairwise(report):
        if abs(b - a) > 3 or abs(b - a) < 1:
            return False
        if descending and b > a:
            return False
        elif not descending and b < a:
            return False
    return True


def can_heal(report):
    n = len(report)
    for i in range(n):
        candidate = report[:i] + report[i + 1 :]
        if is_safe(candidate):
            return True
    return False


def count(reports, with_healing=False):
    safe = sum(1 for report in reports if is_safe(report))
    healed = 0
    if with_healing:
        healed = sum(
            1 for report in reports if not is_safe(report) and can_heal(report)
        )
    return safe + healed


def main():
    reports = parse()
    print(f"Part 1: {count(reports)}")
    print(f"Part 2: {count(reports, with_healing=True)}")


if __name__ == "__main__":
    main()
