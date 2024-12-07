import fileinput
from collections import deque
from functools import cache


def parse():
    equations = []
    for line in fileinput.input():
        t, os = line.strip().split(":")
        equations.append((int(t), [int(n) for n in os.split()]))
    return equations


@cache
def generate(size, operators=None):
    if operators is None:
        operators = "+*"
    all = set()
    queue = deque(operators)
    while queue:
        item = queue.popleft()
        if len(item) == size:
            all.add(item)
            continue
        for op in operators:
            queue.append(item + op)
    return list(all)


def eval(test, operands, operators):
    queue = deque(operands)
    for operator in operators:
        a, b = queue.popleft(), queue.popleft()
        if operator == "+":
            queue.appendleft(a + b)
        elif operator == "*":
            queue.appendleft(a * b)
        elif operator == "|":
            queue.appendleft(int(str(a) + str(b)))
    return test == queue.popleft()


def calibrations(equations, operators=None):
    if operators is None:
        operators = "+*"
    calibration = 0
    for test, operands in equations:
        for ops in generate(len(operands) - 1, operators):
            if eval(test, operands, ops):
                calibration += test
                break
    return calibration


def main():
    equations = parse()
    print(f"Part 1: {calibrations(equations)}")
    operators = "+*|"
    print(f"Part 2: {calibrations(equations, operators=operators)}")


if __name__ == "__main__":
    main()
