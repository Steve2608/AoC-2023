import unittest

from day06 import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""Time:      7  15   30
Distance:  9  40  200"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(288, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data)
        self.assertEqual(71503, p2)


if __name__ == "__main__":
    unittest.main()
