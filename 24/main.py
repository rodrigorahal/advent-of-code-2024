from collections import deque
import fileinput
from itertools import combinations


def parse():
    wires = {}
    gates = set()
    S = ""
    for line in fileinput.input():
        S += line
    top, bottom = S.split("\n\n")

    for line in top.split("\n"):
        wire, val = line.split(": ")
        wires[wire] = int(val)

    for line in bottom.split("\n"):
        ins, out = line.split(" -> ")
        a, op, b = ins.split()
        gates.add((a, op, b, out))
        for wire in (a, b, out):
            if wire not in wires:
                wires[wire] = None
    return wires, gates


def produce(wires, a, op, b):
    if op == "AND":
        return int(wires[a] and wires[b])
    if op == "OR":
        return int(wires[a] or wires[b])
    if op == "XOR":
        return int((wires[a] and not wires[b]) or (wires[b] and not wires[a]))


def solve(wires, gates):
    to_solve = deque(gates)
    # while to_solve:
    for _ in range(12_000):
        if not to_solve:
            break
        curr = to_solve.popleft()
        a, op, b, out = curr
        if wires[a] is not None and wires[b] is not None:
            # if out == "rvh" or out == "z01":
            #     print(out, a, op, b, wires[a], wires[b], produce(wires, a, op, b))
            wires[out] = produce(wires, a, op, b)
        else:
            to_solve.append((a, op, b, out))
    return wires


def val(wires, prefix):
    ws = sorted([w for w in wires if w.startswith(prefix)], reverse=True)
    out = "".join(str(wires[w]) for w in ws)
    return out, int(out, 2)


def gates_to(gates_by_out, out):
    seen = set()
    queue = deque([out])
    gates = []
    while queue:
        curr = queue.popleft()
        if curr in seen:
            continue
        seen.add(curr)
        if curr.startswith("x") or curr.startswith("y"):
            continue
        (a, op, b, curr) = gates_by_out[curr]
        # if a.startswith("x") or a.startswith("y"):
        #     continue
        gates.append((a, op, b, curr))
        queue.extend([a, b])
    return gates


def zeros(wires):
    cwires = dict(wires)
    for i in range(45):
        cwires[f"x{i.zfill(2)}"] = 0
        cwires[f"y{i.zfill(2)}"] = 0


def get_candidates(wires, gates, gates_by_out):
    candidates = []
    # by inspecting each x bit individually we can find that
    # these outputs need to swaped
    # i.e when only x08 is on then z09 will be one when z08 should be on
    # we then find try all swaps that would swap those outputs as candidates
    for a, b in [("08", "09"), ("15", "16"), ("22", "23"), ("31", "32")]:
        cwires = dict(wires)
        to_za = gates_to(gates_by_out, f"z{a}")
        to_zb = gates_to(gates_by_out, f"z{b}")

        for i in range(45):
            cwires[f"x{str(i).zfill(2)}"] = 0
            cwires[f"y{str(i).zfill(2)}"] = 0

        cwires[f"y{a}"] = 1

        oowires = solve(dict(cwires), gates)

        assert val(oowires, "z")[1] != val(oowires, "x")[1] + val(oowires, "y")[1]

        for a, b in combinations(to_za + to_zb, 2):
            if a == b:
                continue
            cgates = set(gates)
            aa, aop, ab, aout = a
            ba, bop, bb, bout = b

            cgates.remove(a)
            cgates.remove(b)
            cgates.add((aa, aop, ab, bout))
            cgates.add((ba, bop, bb, aout))
            try:
                owires = solve(dict(cwires), cgates)
                if (
                    val(oowires, "z")[1] != val(owires, "z")[1]
                    and val(owires, "z")[1] == val(owires, "x")[1] + val(owires, "y")[1]
                ):
                    candidates.append((a, b))
                    # print(f"swapped {a} and {b}")
            except ValueError:
                continue
    return candidates


def solve2(wires, gates, candidates):
    OUTS = set()
    for swaps in combinations(candidates, 4):
        cgates = set(gates)
        for a, b in swaps:
            if a == b:
                continue
            aa, aop, ab, aout = a
            ba, bop, bb, bout = b
            cgates.discard(a)
            cgates.discard(b)
            cgates.add((aa, aop, ab, bout))
            cgates.add((ba, bop, bb, aout))

        try:
            owires = solve(dict(wires), cgates)
            if val(owires, "z")[1] == val(owires, "x")[1] + val(owires, "y")[1]:
                outs = []
                for (aa, aop, ab, aout), (ba, bop, bb, bout) in swaps:
                    outs.append(aout)
                    outs.append(bout)
                if len(outs) == len(set(outs)):
                    OUTS.add(",".join(sorted(outs)))
                # print(",".join(sorted(outs)))
        except ValueError:
            continue
    return OUTS


def find(wires, gates, candidates):
    for i in range(45):
        wires[f"x{str(i).zfill(2)}"] = 1
        wires[f"y{str(i).zfill(2)}"] = 1

    OUTS1 = solve2(wires, gates, candidates)

    for i in range(45):
        wires[f"x{str(i).zfill(2)}"] = 1
        wires[f"y{str(i).zfill(2)}"] = 1
    wires["x02"] = 0
    OUTS2 = solve2(wires, gates, candidates)

    for i in range(45):
        wires[f"x{str(i).zfill(2)}"] = 1
        wires[f"y{str(i).zfill(2)}"] = 0
    wires["x02"] = 0
    wires["x08"] = 1
    wires["x09"] = 0
    OUTS3 = solve2(wires, gates, candidates)

    for i in range(45):
        wires[f"x{str(i).zfill(2)}"] = 1
        wires[f"y{str(i).zfill(2)}"] = 0
    wires["y08"] = 1
    wires["y09"] = 1
    wires["y08"] = 1
    wires["y09"] = 1
    OUTS4 = solve2(wires, gates, candidates)

    assert len(OUTS1 & OUTS2 & OUTS3 & OUTS4) == 1
    return next(iter(OUTS1 & OUTS2 & OUTS3 & OUTS4))


def main():
    wires, gates = parse()
    owires = solve(dict(wires), gates)
    print(f"Part 1: {val(owires, 'z')[1]}")
    gates_by_out = {out: (a, op, b, out) for a, op, b, out in gates}
    candidates = get_candidates(wires, gates, gates_by_out)
    swaps = find(wires, gates, candidates)
    print(f"Part 2: {swaps}")


if __name__ == "__main__":
    main()
