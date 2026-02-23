from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    gen: tuple[int, ...]
    h: int        # height
    w: int        # width


def generate_lattice(bottom: list[int], top: list[int]):
    dims = len(bottom)

    nodes = []
    levels = {}

    def build(current, idx):
        if idx == dims:
            h = sum(current[i] - bottom[i] for i in range(dims))
            node = Node(tuple(current), h=h, w=0)
            levels.setdefault(h, []).append(node)
            return

        for v in range(bottom[idx], top[idx] + 1):
            build(current + [v], idx + 1)

    build([], 0)

    # assegna width index
    for h, level in levels.items():
        for w, node in enumerate(level):
            nodes.append(Node(node.gen, h, w))

    return levels