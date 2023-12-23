from collections import defaultdict, deque

from timing_util import Timing

Point2D = tuple[int, int]


def get_data(data: str) -> tuple[list[str], Point2D, Point2D]:
    grid = data.split("\n")
    src = (0, 1)
    dst = (len(grid) - 1, len(grid[0]) - 2)

    return grid, src, dst


def find_junctions(grid: list[str]) -> set[Point2D]:
    junctions = set()
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i][j] == "#":
                continue

            neighbors = [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
            ]
            if sum(1 for neighbor in neighbors if grid[neighbor[0]][neighbor[1]] != "#") >= 3:
                junctions.add((i, j))

    return junctions


def get_distances(
    grid: list[str], junctions: set[Point2D], respect_junctions: bool
) -> dict[tuple[Point2D, Point2D], int]:
    distances = {}
    for junction in junctions:
        visited = set()
        distance = 0

        curr = junction
        queue: deque[tuple[int, Point2D]] = deque([(0, curr)])
        while queue:
            distance, curr = queue.popleft()
            if curr != junction and curr in junctions:
                distances[(junction, curr)] = distance
                continue
            if curr in visited:
                continue
            visited.add(curr)

            if respect_junctions:
                match grid[curr[0]][curr[1]]:
                    case ".":
                        neighbors = [
                            (curr[0] - 1, curr[1]),
                            (curr[0] + 1, curr[1]),
                            (curr[0], curr[1] - 1),
                            (curr[0], curr[1] + 1),
                        ]
                    case ">":
                        neighbors = [(curr[0], curr[1] + 1)]
                    case "<":
                        neighbors = [(curr[0], curr[1] - 1)]
                    case "^":
                        neighbors = [(curr[0] - 1, curr[1])]
                    case "v":
                        neighbors = [(curr[0] + 1, curr[1])]
                    case _:
                        neighbors = []

            else:
                neighbors = [
                    (curr[0] - 1, curr[1]),
                    (curr[0] + 1, curr[1]),
                    (curr[0], curr[1] - 1),
                    (curr[0], curr[1] + 1),
                ]

            for neighbor in neighbors:
                if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                    continue
                if neighbor in visited:
                    continue
                if grid[neighbor[0]][neighbor[1]] == "#":
                    continue

                queue.insert(0, (distance + 1, neighbor))

    return distances


def get_neighbors(distances: dict[tuple[Point2D, Point2D], int]) -> dict[Point2D, list[Point2D]]:
    neighbors = defaultdict(list)
    for (from_, to), _ in distances.items():
        neighbors[from_].append(to)
    return neighbors


def find_longest_path(grid: list[str], src: Point2D, dst: Point2D, respect_junctions: bool) -> int:
    def longest_path(src: Point2D, dst: Point2D, distance: int, visited: set[Point2D]) -> int:
        if src == dst:
            return distance

        max_dist = 0
        for neigh in neighbors[src]:
            # no circles
            if neigh not in visited:
                visited.add(neigh)
                if (
                    d := longest_path(neigh, dst, distance + distances[(src, neigh)], visited)
                ) > max_dist:
                    max_dist = d
                visited.remove(neigh)

        return max_dist

    junctions = find_junctions(grid) | {src, dst}

    distances = get_distances(grid, junctions, respect_junctions)
    neighbors = get_neighbors(distances)
    return longest_path(src, dst, 0, {src})


def part1(data: tuple[list[str], Point2D, Point2D]) -> int:
    return find_longest_path(*data, respect_junctions=True)


def part2(data: tuple[list[str], Point2D, Point2D]) -> int:
    return find_longest_path(*data, respect_junctions=False)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day23.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
