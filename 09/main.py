import sys

sys.set_int_max_str_digits(0)
import fileinput


def parse():
    return str(fileinput.input().readline())


def blocks(disk):
    b = []
    for i, digit in enumerate(disk):
        if i % 2 == 0:
            for _ in range(int(digit)):
                b.append(str(i // 2))
        else:
            for _ in range(int(digit)):
                b.append(".")
    return b


def compact(blocks):
    j = len(blocks) - 1
    i = 0
    while i < j:
        if blocks[j] == ".":
            j -= 1
            continue
        if blocks[i] != ".":
            i += 1
            continue
        blocks[i], blocks[j] = blocks[j], blocks[i]
        i += 1
        j -= 1
    return blocks


def compact_wo_frag(blocks):
    j = len(blocks) - 1
    block = []
    seen = set()
    while j >= 0:
        if not block:
            if blocks[j] != "." and blocks[j] not in seen:
                block.append(blocks[j])
        elif block:
            if blocks[j] == block[0]:
                block.append(blocks[j])
            else:
                # print(f"{j=}, {block=}, {blocks[j]=}")
                seen.add(block[0])
                search(blocks, block, j + 1)
                # print("===")
                # print("".join(blocks[-10:]))
                # break
                # print("===")
                block = []
                j += 1
        j -= 1
    return blocks


def search(blocks, block, j):
    n = len(block)
    i = 0
    space = []
    # print(f"searching {block=}, {j=}")
    while i < len(blocks):
        # print(f"\t {i=}, {blocks[i]=}")
        if not space:
            if blocks[i] == ".":
                space.append(".")
        elif space:
            if blocks[i] == ".":
                space.append(".")
            else:
                if len(space) >= len(block) and i - len(space) + n < j + n:
                    # print(
                    #     f"{i,j=} {space=}, {block=}, {blocks[i - len(space) : i - len(space) + n]=}, {blocks[j : j + n]=}, {space[:n]=}"
                    # )
                    assert i - len(space) < j + n
                    blocks[i - len(space) : i - len(space) + n], blocks[j : j + n] = (
                        block,
                        space[:n],
                    )
                    break
                else:
                    space = []
        i += 1


def checksum(blocks):
    return sum(i * int(id) for i, id in enumerate(blocks) if id != ".")


def main():
    disk = parse()
    print(f"Part 1: {checksum(compact(blocks(disk)))}")
    print(f"Part 2: {checksum(compact_wo_frag(blocks(disk)))}")


if __name__ == "__main__":
    main()
