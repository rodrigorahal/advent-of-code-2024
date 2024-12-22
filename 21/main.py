from collections import deque, defaultdict
from itertools import pairwise
from functools import cache
import fileinput


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""


NUM_PAD_GRID = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""


DIR_PAD_GRID = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]

DIRS = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}

COORDS = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def search(grid, srow, scol, moves):
    H, W = len(grid), len(grid[0])
    queue = deque([(srow, scol, "")])

    while queue:
        row, col, path = queue.popleft()
        if (grid[srow][scol], grid[row][col]) in moves:
            if len(path) > len(min(moves[(grid[srow][scol], grid[row][col])], key=len)):
                continue
        moves[(grid[srow][scol], grid[row][col])].append(path)

        for dr, dc, mov in [
            (0, 1, ">"),
            (0, -1, "<"),
            (-1, 0, "^"),
            (1, 0, "v"),
        ]:
            nrow, ncol = row + dr, col + dc
            if 0 <= nrow < H and 0 <= ncol < W and grid[nrow][ncol] != " ":
                queue.append((nrow, ncol, path + mov))
    return moves


def invert(dir):
    return {"^": "v", ">": "<", "<": ">", "v": "^"}[dir]


def parse():
    codes = []
    for line in fileinput.input():
        codes.append(line.strip())
    return codes


def numpad_to_dirpad(movements, numpad_paths):
    candidates = [[]]
    for frm, to in pairwise("A" + movements):
        paths = numpad_paths[(frm, to)]
        new_candidates = []
        while candidates:
            candidate = candidates.pop()
            for path in paths:
                new_candidates.append(candidate + [path])
        candidates = new_candidates
    new_candidates = []
    for candidate in candidates:
        new_candidates.append("".join(m + "A" for m in candidate))
    return new_candidates


def expand(movements):
    if len(movements) < 2:
        return ""

    if len(movements) == 2:
        frm, to = movements
        path = MINDIRPAD_PATHS[(frm, to)][0]
        return path + "A"
    return expand(movements[0] + movements[1]) + expand(movements[1:])


def dirpad_to_dirpad(movements, dirpad_paths):
    candidates = [[]]
    movements = "A" + movements
    for i in range(len(movements) - 1):
        frm, to = movements[i], movements[i + 1]
        paths = dirpad_paths[(frm, to)]
        new_candidates = []
        while candidates:
            candidate = candidates.pop()
            for path in paths:
                new_candidates.append(candidate + [path])
        candidates = new_candidates
    new_candidates = []
    for candidate in candidates:
        new_candidates.append("".join(m + "A" for m in candidate))
    return new_candidates


def press(movements, srow, scol, grid):
    pressed = []
    row, col = srow, scol
    for mov in movements:
        if mov == "A":
            pressed.append(grid[row][col])
            continue
        dr, dc = DIRS[mov]
        row, col = row + dr, col + dc
    return pressed


@cache
def cost(path):
    c = 0
    for frm, to in pairwise(path):
        frow, fcol = COORDS[frm]
        trow, tcol = COORDS[to]
        c += abs(trow - frow) + abs(tcol - fcol)
    return c


@cache
def solve(seq, level, pads=2):
    if level > pads:
        return len(seq)
    S = 0
    for f, t in zip("A" + seq, seq):
        if level == 0:
            paths = NUMPAD_PATHS[(f, t)]
            S += min(solve(path + "A", level + 1, pads) for path in paths)
        else:
            paths = DIRPAD_PATHS[(f, t)]
            S += min(solve(path + "A", level + 1, pads) for path in paths)
    return S


def generate(code, numpad_paths, pads):
    candidates = numpad_to_dirpad(code, numpad_paths)
    for _ in range(pads):
        cc = set()
        for c in candidates:
            # ccs = dirpad_to_dirpad(c, DIRPAD_PATHS)
            ccs = expand("A" + c)
            cc.add(ccs)
            # for i in ccs:
            #     # print(i)
            #     cc.add(i)
        candidates = cc
    sequence = min(cc, key=len)
    minlen = len(sequence)
    return minlen


def main():
    codes = parse()

    global DIRPAD_PATHS
    DIRPAD_PATHS = defaultdict(list)
    for row, col in [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
        search(DIR_PAD_GRID, row, col, DIRPAD_PATHS)

    global NUMPAD_PATHS
    NUMPAD_PATHS = defaultdict(list)
    for row, cols in enumerate(NUM_PAD_GRID):
        for col, char in enumerate(cols):
            if char == " ":
                continue
            search(NUM_PAD_GRID, row, col, NUMPAD_PATHS)

    # not correct for 25 pads?
    global MINDIRPAD_PATHS
    MINDIRPAD_PATHS = defaultdict(list)
    for (frm, to), paths in DIRPAD_PATHS.items():
        mincost = min(paths, key=cost)
        MINDIRPAD_PATHS[(frm, to)] = [mincost]

    s = 0
    for code in codes:
        size = generate(code, NUMPAD_PATHS, pads=2)
        s += size * int(code[:-1])
    print(f"Part 1: {s}")

    s = 0
    for code in codes:
        s += solve(code, 0, pads=25) * int(code[:-1])
    print(f"Part 2: {s}")


if __name__ == "__main__":
    main()
