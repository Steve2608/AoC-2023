from timing_util import Timing


def get_data(data: str) -> list[str]:
    return data.split("\n")


def follow_path(
    data: list[str], x: int, y: int, direction: str, already_visited: set[tuple[int, int, str]]
):
    Y, X = len(data), len(data[0])
    while 0 <= y < Y and 0 <= x < X:
        if (key := (x, y, direction)) in already_visited:
            return
        already_visited.add(key)

        match direction:
            case "right":
                match data[y][x]:
                    case "|":
                        follow_path(data, x, y - 1, "up", already_visited)
                        follow_path(data, x, y + 1, "down", already_visited)
                    case "-":
                        x += 1
                    case "/":
                        y -= 1
                        direction = "up"
                    case "\\":
                        y += 1
                        direction = "down"
                    case ".":
                        x += 1
            case "left":
                match data[y][x]:
                    case "|":
                        follow_path(data, x, y - 1, "up", already_visited)
                        follow_path(data, x, y + 1, "down", already_visited)
                    case "-":
                        x -= 1
                    case "/":
                        y += 1
                        direction = "down"
                    case "\\":
                        y -= 1
                        direction = "up"
                    case ".":
                        x -= 1
            case "up":
                match data[y][x]:
                    case "|":
                        y -= 1
                    case "-":
                        follow_path(data, x + 1, y, "right", already_visited)
                        follow_path(data, x - 1, y, "left", already_visited)
                    case "/":
                        x += 1
                        direction = "right"
                    case "\\":
                        x -= 1
                        direction = "left"
                    case ".":
                        y -= 1
            case "down":
                match data[y][x]:
                    case "|":
                        y += 1
                    case "-":
                        follow_path(data, x + 1, y, "right", already_visited)
                        follow_path(data, x - 1, y, "left", already_visited)
                    case "/":
                        x -= 1
                        direction = "left"
                    case "\\":
                        x += 1
                        direction = "right"
                    case ".":
                        y += 1


def path_length(data: list[str], x: int, y: int, direction: str) -> int:
    already_visited = set()
    follow_path(data, x, y, direction, already_visited)
    return len(set((x, y) for x, y, _ in already_visited))


def part1(data: list[str]) -> int:
    return path_length(data, 0, 0, "right")


def part2(data: list[str]) -> int:
    def stream_path_lengths(data: list[str]):
        max_y, max_x = len(data) - 1, len(data[0]) - 1
        for y in range(len(data)):
            yield path_length(data, 0, y, "right")
            yield path_length(data, max_x, y, "left")

        for x in range(len(data[0])):
            yield path_length(data, x, 0, "down")
            yield path_length(data, x, max_y, "up")

    return max(stream_path_lengths(data))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day16.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
