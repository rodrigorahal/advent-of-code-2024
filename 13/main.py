import fileinput


def parse():
    machines = []
    S = ""
    for line in fileinput.input():
        S += line

    blocks = S.split("\n\n")
    for block in blocks:
        machine = []
        for line in block.split("\n"):
            """
            Button A: X+94, Y+34
            Button B: X+22, Y+67
            Prize: X=8400, Y=5400
            """
            if line.startswith("Prize:"):
                left, right = line.strip("Prize: ").split(", ")
                X = left.strip("X=")
                Y = right.strip("Y=")
                machine.append((int(X), int(Y)))
            else:
                left, right = line[11:].split(", ")
                X = left.strip("X+")
                Y = right.strip("Y+")
                machine.append((int(X), int(Y)))
        machines.append(machine)
    return machines


def search(machine, limit=100):
    A, B, P = machine
    dxa, dya = A
    dxb, dyb = B
    x, y = 0, 0
    costs = []
    for i in range(limit + 1):
        for j in range(limit + 1):
            X = x + (i * dxa) + (j * dxb)
            Y = y + (i * dya) + (j * dyb)
            if (X, Y) == P:
                costs.append((3 * i) + (1 * j))
    return min(costs) if costs else 0


def maths(machine):
    """
    the math is mathing:

    Given the system of equations

    |DXa  DXb| |i| = |Px|
    |DYa  DYb| |j|   |Py|

    where we want to find out i,j that satisfy the equation
    for the given (DXa, DYa), (DXb, DYb), (Px, Py)

    let the matrix be M
    If Det(M) != 0 then we can invert the matrix to find
    M^-1 . P = (i,j) i.e

    i = ((Px * DYb) - (Py * DXb)) / Det
    j = ((Py * DXa) - (Px * DYa)) / Det
    """
    A, B, P = machine
    dxa, dya = A
    dxb, dyb = B
    px, py = P
    px += 10000000000000
    py += 10000000000000
    D = dxa * dyb - dxb * dya
    i = ((px * dyb) - (py * dxb)) / D
    j = ((py * dxa) - (px * dya)) / D
    if int(i) == i and int(j) == j:
        return int((3 * i) + j)
    return 0


def main():
    machines = parse()
    print(f"Part 1: {sum([search(machine) for machine in machines])}")
    print(f"Part 2: {sum(maths(machine) for machine in machines)}")


if __name__ == "__main__":
    main()
