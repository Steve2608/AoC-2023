from timing_util import Timing


def get_data(content: str) -> list[tuple[str, list[int]]]:
    data = []
    for line in content.splitlines():
        record, groups = line.split()
        groups = list(map(int, groups.split(",")))
        data.append((record, groups))

    return data


def sol(record: str, groups: list[int]) -> int:
    def solve(r_i: int, g_i: int, streak: int) -> int:
        if (state := (r_i, g_i, streak)) in cache:
            # if superpositions converge, we only need to compute one of them
            return cache[state]

        if r_i >= R:
            # record is exhausted and we have consumed all groups
            if not streak and g_i == G:
                return 1
            # we finished on a complete streak
            elif g_i == G - 1 and streak == groups[g_i]:
                return 1
            # superposition did not work -> no solution was found
            else:
                return 0

        n = 0
        match record[r_i]:
            case ".":
                if not streak:
                    # no streak before, just advance one in record
                    n = solve(r_i + 1, g_i, 0)
                elif g_i < G and groups[g_i] == streak:
                    # if current streak of '#' is over, advance one in record and arrangements
                    n = solve(r_i + 1, g_i + 1, 0)
            case "#":
                # advance one in record and current streak
                n = solve(r_i + 1, g_i, streak + 1)
            case "?":
                # for '?' we superposition the two cases above
                if not streak:
                    n = solve(r_i + 1, g_i, 0)
                elif g_i < G and groups[g_i] == streak:
                    n = solve(r_i + 1, g_i + 1, 0)

                n += solve(r_i + 1, g_i, streak + 1)

        cache[state] = n
        return n

    R, G = len(record), len(groups)
    cache = {}
    return solve(r_i=0, g_i=0, streak=0)


def part1(data: list[tuple[str, list[int]]]) -> int:
    return sum(sol(record, groups) for record, groups in data)


def part2(data: list[tuple[str, list[int]]]) -> int:
    return sum(sol("?".join([record] * 5), groups * 5) for record, groups in data)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day12.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
