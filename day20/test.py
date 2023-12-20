import unittest

from day20.sol import get_data, part1, part2


class AoCTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.data = get_data(
            r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
        )
        self.data2 = get_data(
            r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
        )

    def test_part1(self) -> None:
        p1 = part1(self.data)
        self.assertEqual(32000000, p1)
        p1 = part1(self.data2)
        self.assertEqual(11687500, p1)


if __name__ == "__main__":
    unittest.main()
