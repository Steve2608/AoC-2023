import collections
import dataclasses as dc
from functools import total_ordering

from timing_util import Timing


@total_ordering
@dc.dataclass(slots=True)
class Hand:
    cards: str
    bid: int
    jacks_are_jokers: bool = False

    card_values: tuple[int] = dc.field(init=False)
    best_hand: str = dc.field(init=False)
    _n_unique_same: tuple[int, int] = dc.field(init=False)

    def __post_init__(self) -> None:
        def _n_unique_same(self) -> tuple[int, int]:
            counter = collections.Counter(self.best_hand)
            most_of_a_kind = max(counter.values())
            return len(counter), most_of_a_kind
        
        def best_hand(self) -> str:
            if not self.jacks_are_jokers or "J" not in self.cards:
                return self.cards

            counts = collections.Counter(self.cards)
            # remove jacks
            if counts.pop("J") == 5:
                # if hand is all jacks return 5 aces
                return "A" * 5

            best_card = max(counts, key=lambda k: (counts.get(k), self.card_value(k)))
            return "".join(card if card != "J" else best_card for card in self.cards)
        
        self.card_values = tuple(map(self.card_value, self.cards))
        self.best_hand = best_hand(self)
        self._n_unique_same = _n_unique_same(self)

    def __lt__(self, other: "Hand") -> bool:
        n_unique_self, n_same_self = self._n_unique_same
        n_unique_other, n_same_other = other._n_unique_same

        # self has less cards of same suit than other
        if n_same_self < n_same_other:
            return True
        # self has more cards of same suit than other
        elif n_same_self > n_same_other:
            return False
        # self has different amount of unique cards -> one has to have better hand
        elif n_unique_self != n_unique_other:
            # if self has more unique cards than other, it has to be worse
            return n_unique_self > n_unique_other
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
