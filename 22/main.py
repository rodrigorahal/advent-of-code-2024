import fileinput
from collections import deque, defaultdict


def parse():
    secrets = []
    for line in fileinput.input():
        secrets.append(int(line.strip()))
    return secrets


def gen(secret, n):
    price_by_sequence = defaultdict(list)
    sequence = deque([])
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
            price_by_sequence[tuple(sequence)].append(price)
        else:
            sequence.append(diff)
            if len(sequence) == 4:
                price_by_sequence[tuple(sequence)].append(price)
    return secret, price_by_sequence


def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def search(secrets):
    sequences = set()
    prices = []
    for secret in secrets:
        _, prices_by_seq = gen(secret, n=2000)
        prices.append(prices_by_seq)
        sequences.update(prices_by_seq.keys())

    maxprice = float("-inf")
    for j, seq in enumerate(sequences):
        # if j % 1000 == 0:
        #     print(j, maxprice)
        P = sum(price_by_seq[seq][0] for price_by_seq in prices if price_by_seq[seq])
        maxprice = max(maxprice, P)
    return maxprice


def main():
    secrets = parse()
    print(f"Part 1: {sum(gen(s, n=2000)[0] for s in secrets)}")
    print(f"Part 2: {search(secrets)}")


if __name__ == "__main__":
    main()
