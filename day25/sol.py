import random

from timing_util import Timing

Vertex = str
Edge = tuple[Vertex, Vertex]


def get_data(data: str) -> tuple[set[Vertex], set[Edge]]:
    vertices = set()
    edges = set()
    for line in data.splitlines():
        src, dst = line.split(": ")
        dst = dst.split(" ")

        vertices.add(src)
        vertices.update(dst)

        edges.update((src, d) for d in dst)
    return vertices, edges


def kargers_algorithm(V: set[Vertex], E: set[Edge]) -> int:
    def is_3_cut() -> bool:
        return sum(vertex_to_component[u] != vertex_to_component[v] for u, v in E) == 3

    def contract_edge(edge: Edge):
        v1, v2 = edge
        c1 = vertex_to_component[v1]
        c2 = vertex_to_component[v2]

        if c1 is not c2:
            c1.update(c2)
            components.remove(c2)
            for v in c2:
                vertex_to_component[v] = c1

    # we need E as a list for random.choice
    E: list[Edge] = list(E)
    while True:
        components = [{v} for v in V]
        vertex_to_component = {v: c for c in components for v in c}

        while len(components) > 2:
            contract_edge(random.choice(E))

        if is_3_cut():
            return len(components[0]) * len(components[1])


def part1(data: tuple[set[Vertex], set[Edge]]) -> int:
    vertices, edges = data
    return kargers_algorithm(vertices, edges)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day25.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
