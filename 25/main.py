import fileinput


def parse():
    locks = []
    keys = []
    S = ""
    for line in fileinput.input():
        S += line

    blocks = S.split("\n\n")

    for block in blocks:
        item = []
        for line in block.split("\n"):
            item.append(line)
        if block.startswith("#"):
            locks.append(item)
        else:
            keys.append(item)
    return locks, keys


def display(grid):
    for row in grid:
        print(row, sep="")
    print()


def lock_to_heights(lock):
    heights = []
    H, W = len(lock), len(lock[0])
    for col in range(W):
        h = 0
        for row in range(H):
            if lock[row][col] == ".":
                heights.append(h - 1)
                break
            h += 1
    return heights


def key_to_heights(key):
    heights = []
    H, W = len(key), len(key[0])
    for col in range(W):
        h = 0
        for row in range(H - 1, -1, -1):
            if key[row][col] == ".":
                heights.append(h - 1)
                break
            h += 1
    return heights


def matches(locks, keys):
    c = 0
    locks_heights = [lock_to_heights(lock) for lock in locks]
    keys_heights = [key_to_heights(key) for key in keys]

    for lock in locks_heights:
        for key in keys_heights:
            if all(a + b < 6 for a, b in zip(lock, key)):
                c += 1
    return c


def main():
    locks, keys = parse()
    print(f"Part 1: {matches(locks, keys)}")


if __name__ == "__main__":
    main()
