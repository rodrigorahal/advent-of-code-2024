import fileinput
from collections import Counter


def parse():
    left, right = [], []
    for line in fileinput.input():
        a, b = line.strip().split()
        left.append(int(a))
        right.append(int(b))
    return list(sorted(left)), list(sorted(right))


def dist(left, right):
    return sum(abs(b - a) for a, b in zip(left, right))


def similarity(left, right):
    count = Counter(right)
    return sum(a * count[a] for a in left)


def main():
    left, right = parse()
    print(f"Part 1: {dist(left, right)}")
    print(f"Part 2: {similarity(left, right)}")


if __name__ == "__main__":
    main()
