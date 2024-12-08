import fileinput
from collections import defaultdict


def parse():
    grid = []
    antennas = defaultdict(list)
    for row, line in enumerate(fileinput.input()):
        grid.append(line.strip())
        for col, char in enumerate(line.strip()):
            if char == ".":
                continue
            antennas[char].append((row, col))
    return grid, antennas


def antinodes(a, b):
    arow, acol = a
    brow, bcol = b

    dr = brow - arow
    dc = bcol - acol

    return [(arow - dr, acol - dc), (brow + dr, bcol + dc)]


def find(grid, antennas):
    H, W = len(grid), len(grid[0])
    seen = set()
    for coords in antennas.values():
        for i, a in enumerate(coords):
            for b in coords[i + 1 :]:
                for arow, acol in antinodes(a, b):
                    if 0 <= arow < H and 0 <= acol < W:
                        seen.add((arow, acol))
    return len(seen)


def lines(antennas):
    ls = []
    for coords in antennas.values():
        for i, a in enumerate(coords):
            for b in coords[i + 1 :]:
                arow, acol = a
                brow, bcol = b
                ls.append((arow, acol, brow - arow, bcol - acol))
    return ls


def on_line(row, col, lrow, lcol, dr, dc):
    DR, DC = row - lrow, col - lcol
    if dr and dc:
        return DR * dc == DC * dr and DR % dr == 0
    if dr:
        return DR % dr == 0
    if dc:
        return DC % dc == 0


def intercept(grid, antennas):
    H, W = len(grid), len(grid[0])
    ls = lines(antennas)
    count = 0
    for row in range(H):
        for col in range(W):
            for line in ls:
                if on_line(row, col, *line):
                    count += 1
                    break
    return count


def display(grid):
    for row in grid:
        print(row)


def main():
    grid, antennas = parse()
    print(f"Part 1: {find(grid, antennas)}")
    print(f"Part 2: {intercept(grid, antennas)}")


if __name__ == "__main__":
    main()
