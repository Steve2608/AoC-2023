import dataclasses

from timing_util import Timing


@dataclasses.dataclass(slots=True)
class Ticket:
    ticket_id: int
    want: set[int]
    have: set[int]
    winning: set[int] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.winning = self.want & self.have


def get_data(content: str) -> list[Ticket]:
    tickets = []
    for line in content.split("\n"):
        colon_idx = line.index(":")
        pipe_idx = line.index("|")
        ticket_id = int(line[len("Card ") : colon_idx].lstrip())

        want_numbers = set(map(int, line[colon_idx + 1 : pipe_idx - 1].lstrip().split()))
        have_numbers = set(map(int, line[pipe_idx + 1 :].split()))

        ticket = Ticket(ticket_id, want=want_numbers, have=have_numbers)
        tickets.append(ticket)

    return tickets


def part1(data: list[Ticket]) -> int:
    def score(ticket: Ticket) -> int:
        if len(ticket.winning) > 0:
            return 1 << (len(ticket.winning) - 1)
        return 0

    return sum(map(score, data))


def part2(data: list[Ticket]) -> int:
    def card_tree(ticket_id: int, lookup: dict[int, int]) -> int:
        ticket = ticket_map[ticket_id]
        n_winning = len(ticket.winning)

        n = 1
        for i in range(ticket_id + 1, ticket_id + 1 + n_winning):
            if not lookup[i]:
                n += card_tree(i, lookup)
            else:
                n += lookup[i]

        lookup[ticket_id] = n
        return n

    # since ticket.id is 1-indexed create one extra element at the start
    ticket_map = [None] + data
    lookup = [0] + [0] * len(data)

    for ticket in data:
        card_tree(ticket.ticket_id, lookup)

    return sum(lookup)


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day04.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
