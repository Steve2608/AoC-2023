import unittest

from day08.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data1 = get_data(
            r"""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
        )

        self.data2 = get_data(
            r"""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
        )

        self.data3 = get_data(
            r"""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data1)
        self.assertEqual(2, p1)
        p1 = part1(self.data2)
        self.assertEqual(6, p1)

    def test_part2(self) -> None:
        p2 = part2(self.data3)
        self.assertEqual(6, p2)


if __name__ == "__main__":
    unittest.main()
