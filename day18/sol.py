from typing import Literal

from timing_util import Timing

Direction = Literal["R", "L", "D", "U"]
Point2D = tuple[int, int]


def get_data(data: str) -> list[str]:
    return data.split("\n")


def get_vertices(lines: list[tuple[Direction, int]]) -> list[Point2D]:
    curr = (0, 0)
    vertices: list[Point2D] = [curr]
    for direction, distance in lines:
        match direction:
            case "R":
                curr = (curr[0] + distance, curr[1])
            case "L":
                curr = (curr[0] - distance, curr[1])
            case "D":
                curr = (curr[0], curr[1] + distance)
            case "U":
                curr = (curr[0], curr[1] - distance)
        vertices.append(curr)
    return vertices


def trench_area(vertices: list[Point2D]) -> int:
    def shoelace_area(vertices: list[Point2D]) -> int:
        N = len(vertices)
        area = 0

        for i in range(N - 1):
            area += vertices[i][0] * vertices[i + 1][1] - vertices[i][1] * vertices[i + 1][0]
        area += vertices[N - 1][0] * vertices[0][1] - vertices[N - 1][1] * vertices[0][0]

        return abs(area) // 2

    def circumference(vertices: list[Point2D]) -> int:
        circumference = 0
        for i in range(len(vertices) - 1):
            circumference += abs(vertices[i][0] - vertices[i + 1][0]) + abs(
                vertices[i][1] - vertices[i + 1][1]
            )
        return circumference

    return shoelace_area(vertices) + circumference(vertices) // 2 + 1


def part1(data: list[str]) -> int:
    def parse_data(data: list[str]) -> list[tuple[Direction, int]]:
        lines = []
        for line in data:
            direction, distance, _ = line.split()
            lines.append((direction, int(distance)))
        return lines

    return trench_area(get_vertices(parse_data(data)))


def part2(data) -> int:
    def parse_data(data: list[str]) -> list[tuple[Direction, int]]:
        lines = []
        for line in data:
            direction, _, color = line.split()
            color = color[2:-1]

            match color[-1]:
                case "0":
                    direction = "R"
                case "1":
                    direction = "D"
                case "2":
                    direction = "L"
                case "3":
                    direction = "U"
            lines.append((direction, int(color[:-1], base=16)))
        return lines

    return trench_area(get_vertices(parse_data(data)))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day18.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
