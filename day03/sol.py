from timing_util import Timing


def get_data(content: str) -> list[list[str | int]]:
    lines = []
    for line in content.split("\n"):
        curr_line = []
        i = 0
        while i < len(line):
            num = 0
            if line[i].isdigit():
                j = i
                while j < len(line) and line[j].isdigit():
                    num = num * 10 + int(line[j])
                    j += 1
                while i < j:
                    curr_line.append(num)
                    i += 1
            else:
                curr_line.append(line[i])
                i += 1
        lines.append(curr_line)
    return lines


def part1(data: list[list[str | int]]) -> int:
    s = 0
    for i, x in enumerate(data):
        for j, char in enumerate(x):
            if char == ".":
                continue
            if isinstance(data[i][j], int):
                continue

            for k in (i - 1, i, i + 1):
                # new line always ends previous number
                prev_was_number = False
                for l in (j - 1, j, j + 1):
                    if k < 0 or k >= len(data) or l < 0 or l >= len(data[k]):
                        continue
                    if k == i and l == j:
                        # center point always ends previous number
                        prev_was_number = False
                        continue

                    if isinstance(data[k][l], int):
                        if not prev_was_number:
                            s += data[k][l]  # pyright: ignore[reportGeneralTypeIssues]
                        prev_was_number = True
                    else:
                        prev_was_number = False

    return s


def part2(data: list[list[str | int]]) -> int:
    gear_sum = 0
    for i, x in enumerate(data):
        for j, char in enumerate(x):
            if char != "*":
                continue

            gears = []
            for k in (i - 1, i, i + 1):
                # new line always ends previous number
                prev_was_number = False
                for l in (j - 1, j, j + 1):
                    if k < 0 or k >= len(data) or l < 0 or l >= len(data[k]):
                        continue
                    # center point always ends previous number
                    if k == i and l == j:
                        prev_was_number = False
                        continue

                    if isinstance(data[k][l], int):
                        if not prev_was_number:
                            gears.append(data[k][l])
                        prev_was_number = True
                    else:
                        prev_was_number = False

            if len(gears) == 2:
                gear_sum += gears[0] * gears[1]

    return gear_sum


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day03.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
