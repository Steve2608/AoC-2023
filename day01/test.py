import unittest

from day01.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data1 = get_data(
            r"""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
        )
        self.data2 = get_data(
            r"""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data1)
        self.assertEqual(142, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data2)
        self.assertEqual(281, p2)


if __name__ == "__main__":
    unittest.main()
