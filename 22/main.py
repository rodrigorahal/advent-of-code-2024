import fileinput
from collections import deque, defaultdict


def parse():
    secrets = []
    for line in fileinput.input():
        secrets.append(int(line.strip()))
    return secrets


def gen(secret, n, price_by_seq):
    sequence = deque([])
    seen = set()
    price = secret % 10
    for i in range(n):
        secret = prune(mix(secret, secret * 64))
        secret = prune(mix(secret, secret // 32))
        secret = prune(mix(secret, secret * 2048))
        nprice = secret % 10
        diff = nprice - price
        price = nprice
        if len(sequence) == 4:
            sequence.popleft()
            sequence.append(diff)
            if tuple(sequence) in seen:
                continue
            price_by_seq[tuple(sequence)] += price
            seen.add(tuple(sequence))
        else:
            sequence.append(diff)
            if len(sequence) == 4:
                if tuple(sequence) in seen:
                    continue
                price_by_seq[tuple(sequence)] += price
                seen.add(tuple(sequence))
    return secret


def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def search(secrets):
    price_by_seq = defaultdict(int)
    for secret in secrets:
        gen(secret, n=2000, price_by_seq=price_by_seq)
    return max(price_by_seq.values())


def main():
    secrets = parse()
    print(
        f"Part 1: {sum(gen(s, n=2000, price_by_seq=defaultdict(int)) for s in secrets)}"
    )
    print(f"Part 2: {search(secrets)}")


if __name__ == "__main__":
    main()
