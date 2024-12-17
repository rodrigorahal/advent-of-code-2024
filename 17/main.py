import fileinput


def parse():
    mem = []
    S = ""
    for line in fileinput.input():
        S += line

    blocks = S.split("\n\n")
    top, bottom = blocks

    for line in top.split("\n"):
        mem.append(int(line[12:]))

    program = [int(n) for n in bottom[9:].split(",")]
    return mem, program


def val(operand, mem):
    if operand in (0, 1, 2, 3):
        return operand
    if operand in (4, 5, 6):
        return mem[operand - 4]
    else:
        raise ValueError(f"{operand=}, {mem=}")


def run(program, mem):
    outputs = []
    i = 0
    while i < len(program):
        opcode, operand = program[i], program[i + 1]
        if opcode == 0:
            mem[0] = int(mem[0] / pow(2, val(operand, mem)))
        if opcode == 1:
            mem[1] = mem[1] ^ operand
        if opcode == 2:
            mem[1] = val(operand, mem) % 8
        if opcode == 3:
            if not mem[0] == 0:
                i = operand
                continue
        if opcode == 4:
            mem[1] = mem[1] ^ mem[2]
        if opcode == 5:
            outputs.append(val(operand, mem) % 8)
        if opcode == 6:
            mem[1] = int(mem[0] / pow(2, val(operand, mem)))
        if opcode == 7:
            mem[2] = int(mem[0] / pow(2, val(operand, mem)))
        i += 2
    return outputs, mem


def search(program):
    """
    We need A to produce 16 loops of the program
    Each loop will produce an output value
    And at each loop we only analyze A % 8
    Here we construct A in reverse order:
    'What A is required to produce the last value(s) in the program?'
    Once we find that we multiply A by 8 and keep searching
    Not guaranteed to be correct though?
    """
    A = 0
    for i in range(1, len(program) + 1):
        target = program[-i:]
        while True:
            outputs, _ = run(program, [A, 0, 0])
            if outputs == target:
                A *= 8
                break
            A += 1
    return A // 8


def main():
    mem, program = parse()
    outputs, _ = run(program, mem)
    print(f"Part 1: {','.join([str(i) for i in outputs])}")
    print(f"Part 2: {search(program)}")


if __name__ == "__main__":
    main()
