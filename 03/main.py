import fileinput
import re


def parse():
    program = []
    for line in fileinput.input():
        program.append(line)
    return program


def extract(program, pattern):
    matches = []
    for line in program:
        m = re.findall(pattern, line)
        matches.extend(m)
    return matches


def apply(instructions):
    valid = []
    enabled = True
    for cmd, a, b in instructions:
        if cmd == "do()":
            enabled = True
        elif cmd == "don't()":
            enabled = False
        elif enabled:
            valid.append((a, b))
    return sum(int(a) * int(b) for a, b in valid)


def main():
    program = parse()

    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    operands = extract(program, pattern)
    print(f"Part 1: {sum(int(a)*int(b) for a, b in operands)}")

    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    instructions = extract(program, pattern)
    print(f"Part 2: {apply(instructions)}")


if __name__ == "__main__":
    main()
