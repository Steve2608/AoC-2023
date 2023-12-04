import dataclasses

from timing_util import Timing


@dataclasses.dataclass(slots=True)
class Game:
    game_id: int
    max_red: int
    max_green: int
    max_blue: int


def get_data(content: str) -> list[Game]:
    games = []
    for line in content.split("\n"):
        colon_idx = line.index(":")
        game_id = int(line[len("Game ") :colon_idx])

        red, green, blue = 0, 0, 0
        for pull in line[colon_idx + 1 :].split(";"):
            for sub_pull in pull.split(","):
                amount, color = sub_pull.strip().split(" ")
                amount = int(amount)
                if color == "red":
                    red = max(amount, red)
                elif color == "green":
                    green = max(amount, green)
                elif color == "blue":
                    blue = max(amount, blue)

        games.append(Game(game_id, red, green, blue))
    return games


def part1(data: list[Game], max_red: int, max_green: int, max_blue: int) -> int:
    def is_valid_game(game: Game) -> int:
        return game.max_red <= max_red and game.max_green <= max_green and game.max_blue <= max_blue

    return sum(game.game_id for game in filter(is_valid_game, data))


def part2(data: list[Game]) -> int:
    return sum(game.max_red * game.max_green * game.max_blue for game in data)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day02.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data, max_red=12, max_green=13, max_blue=14)}")
        print(f"part2: {part2(data)}")
