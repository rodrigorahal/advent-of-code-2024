import fileinput
from collections import deque


def parse():
    S = ""
    for line in fileinput.input():
        S += line

    top, bottom = S.split("\n\n")
    towels = top.split(", ")
    patterns = bottom.split("\n")
    return towels, patterns


def search(towels, pattern):
    queue = deque([(pattern, tuple(), "")])

    while queue:
        to_match, matched, curr = queue.pop()

        if not to_match and curr == pattern:
            return True

        for towel in towels:
            n = len(towel)
            if len(to_match) >= n and to_match[:n] == towel:
                queue.append((to_match[n:], matched + (towel,), curr + towel))
    return False


DP = {}


def ways(towels, to_match, curr=""):
    if to_match == "":
        return 1
    if (to_match, curr) in DP:
        return DP[(to_match, curr)]
    W = 0
    for towel in towels:
        n = len(towel)
        if len(to_match) >= n and to_match[:n] == towel:
            W += ways(towels, to_match[n:], curr + towel)
    DP[(to_match, curr)] = W
    return W


def main():
    towels, patterns = parse()
    print(f"Part 1: {sum(search(towels, pattern) for pattern in patterns)}")
    print(f"Part 2: {sum(ways(towels, pattern) for pattern in patterns)}")


if __name__ == "__main__":
    main()
