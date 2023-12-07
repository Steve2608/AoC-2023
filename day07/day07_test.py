import unittest

from day07 import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(6440, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(5905, p2)


if __name__ == "__main__":
    unittest.main()
