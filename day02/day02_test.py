import unittest

from day02 import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data, max_red=12, max_green=13, max_blue=14)
        self.assertEqual(8, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(2286, p2)


if __name__ == "__main__":
    unittest.main()
