import fileinput
from collections import Counter


def parse():
    return [int(char) for char in fileinput.input().readline().split(" ")]


def blink(stones):
    updated = []
    for stone in stones:
        if stone == 0:
            updated.append(1)
        elif len(str(stone)) % 2 == 0:
            digits = str(stone)
            left, right = digits[: len(digits) // 2], digits[len(digits) // 2 :]
            updated.append(int(left))
            updated.append(int(right))
        else:
            updated.append(stone * 2024)
    return updated


def simulate(stones, n=6):
    curr = stones[:]
    for _ in range(n):
        curr = blink(curr)
    return len(curr)


def blink_by_stone(counter):
    updated = Counter(counter)
    for stone, count in counter.items():
        assert isinstance(stone, int)
        if count == 0:
            del updated[stone]
            continue
        if stone == 0:
            updated[1] += count
            updated[0] -= count
        elif len(str(stone)) % 2 == 0:
            digits = str(stone)
            left, right = digits[: len(digits) // 2], digits[len(digits) // 2 :]
            updated[int(left)] += count
            updated[int(right)] += count
            updated[stone] -= count
        else:
            updated[stone * 2024] += count
            updated[stone] -= count
    return updated


def simulate_by_stone(stones, n=6):
    curr = Counter(stones)
    for _ in range(n):
        curr = blink_by_stone(curr)
    return sum(curr.values())


def main():
    stones = parse()
    print(f"Part 1: {simulate(stones, n=25)}")
    print(f"Part 2: {simulate_by_stone(stones, n=75)}")


if __name__ == "__main__":
    main()
