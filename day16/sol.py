from timing_util import Timing


def get_data(data: str) -> list[list[str]]:
    return [list(line) for line in data.split("\n")]


def follow_path(x: int, y: int, direction: str, already_visited: set[tuple[int, int, str]]):
    # boundary check
    while 0 <= y < len(data) and 0 <= x < len(data[y]):
        if (key := (x, y, direction)) in already_visited:
            return
        already_visited.add(key)

        match direction:
            case "right":
                match data[y][x]:
                    case "|":
                        follow_path(x, y - 1, "up", already_visited)
                        follow_path(x, y + 1, "down", already_visited)
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
                        follow_path(x, y - 1, "up", already_visited)
                        follow_path(x, y + 1, "down", already_visited)
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
                        follow_path(x + 1, y, "right", already_visited)
                        follow_path(x - 1, y, "left", already_visited)
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
                        follow_path(x + 1, y, "right", already_visited)
                        follow_path(x - 1, y, "left", already_visited)
                    case "/":
                        x -= 1
                        direction = "left"
                    case "\\":
                        x += 1
                        direction = "right"
                    case ".":
                        y += 1


def part1(data: list[list[str]]) -> int:
    already_visited = set()
    follow_path(0, 0, "right", already_visited)
    energized = set((x, y) for x, y, _ in already_visited)
    return len(energized)


def part2(data: list[list[str]]) -> int:
    return 0


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day16.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
