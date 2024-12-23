import fileinput
from collections import defaultdict
from itertools import combinations


def parse():
    nodes = set()
    edges = defaultdict(set)
    for line in fileinput.input():
        v, w = line.strip().split("-")
        nodes.add(v)
        nodes.add(w)
        edges[v].add(w)
        edges[w].add(v)
    return nodes, edges


def search(edges, node):
    groups = set()
    for w in edges[node]:
        intrs = edges[node] & edges[w]
        for t in intrs:
            g = tuple(sorted([node, w, t]))
            groups.add(g)
    return groups


def cliques(edges, node):
    groups = set()
    for w in edges[node]:
        intrs = edges[node] & edges[w]
        if len(intrs) > 1:
            nodes = set([node, w])
            nodes |= intrs
            for v, t in combinations(intrs, 2):
                if v not in edges[t]:
                    nodes.discard(v)
                    nodes.discard(t)
            groups.add(tuple(sorted(nodes)))
    return groups


def groups(nodes, edges):
    G = set()
    for node in nodes:
        G.update(search(edges, node))
    return G


def largest(nodes, edges):
    G = set()
    for node in nodes:
        gs = cliques(edges, node)
        G.update(gs)
    return ",".join(max(G, key=len))


def count(groups):
    return sum(any(node.startswith("t") for node in group) for group in groups)


def main():
    nodes, edges = parse()
    print(f"Part 1: {count(groups(nodes, edges))}")
    print(f"Part 2: {largest(nodes, edges)}")


if __name__ == "__main__":
    main()
