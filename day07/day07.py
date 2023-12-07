import collections
import dataclasses
from functools import total_ordering

from timing_util import Timing


@total_ordering
@dataclasses.dataclass(frozen=True)
class Hand:
    cards: str
    bid: int
    jacks_are_jokers: bool = False

    def __lt__(self, other: "Hand") -> bool:
        self_count = collections.Counter(self.best_hand)
        self_of_a_kind = max(self_count.values())

        other_count = collections.Counter(other.best_hand)
        other_of_a_kind = max(other_count.values())

        # other has more cards of same suit than self
        if self_of_a_kind < other_of_a_kind:
            return True
        # self has more cards of same suit than other
        elif self_of_a_kind > other_of_a_kind:
            return False
        # if self has more unique cards than other, it has to be worse
        elif len(self_count) != len(other_count):
            return len(self_count) > len(other_count)
        # compare by card value
        else:
            return self.card_values < other.card_values

    def __eq__(self, other: "Hand") -> bool:
        if other is None or not isinstance(other, Hand):
            return False

        return self.cards == other.cards and self.bid == other.bid and self.jacks_are_jokers == other.jacks_are_jokers

    def card_value(self, card: str) -> int:
        match card:
            case "T":
                return 10
            case "J":
                return 11 if not self.jacks_are_jokers else 1
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
            case _:
                return int(card)

    @property
    def card_values(self) -> list[int]:
        return tuple(map(self.card_value, self.cards))

    @property
    def best_hand(self) -> tuple[int]:
        if not self.jacks_are_jokers or "J" not in self.cards:
            return self.cards

        counts = collections.Counter(self.cards)
        # remove jacks
        if counts.pop("J") == 5:
            # if hand is all jacks return 5 aces
            return "A" * 5

        best_card = max(counts, key=lambda k: (counts.get(k), self.card_value(k)))
        return "".join(card if card != "J" else best_card for card in self.cards)


def get_data(content: str) -> list[Hand]:
    def line_to_hand(line: str) -> Hand:
        cards, bid = line.split()
        return Hand(cards, int(bid))

    return list(map(line_to_hand, content.split("\n")))


def part1(data: list[Hand]) -> int:
    # shallow copy
    return sum(rank * hand.bid for rank, hand in enumerate(sorted(data), 1))


def part2(data: list[Hand]) -> int:
    cards = [Hand(hand.cards, hand.bid, jacks_are_jokers=True) for hand in data]
    return sum(rank * hand.bid for rank, hand in enumerate(sorted(cards), 1))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day07.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
