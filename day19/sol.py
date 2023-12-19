import dataclasses as dc

from timing_util import Timing


@dc.dataclass(slots=True, frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


@dc.dataclass
class Workflow:
    name: str
    rules: list[str]

    def __call__(self, Part) -> str:
        # populating locals() so eval can work
        x, m, a, s = Part.x, Part.m, Part.a, Part.s
        for rule in self.rules:
            if ":" in rule:
                if eval(rule[: rule.index(":")]):
                    return rule[rule.index(":") + 1 :]
                continue
            return rule
        raise ValueError("No rule matched")


def get_data(data: str) -> tuple[dict[str, Workflow], list[Part]]:
    workflows, parts = data.split("\n\n")
    wfs = {}
    for line in workflows.split("\n"):
        name = line[: (start := line.index("{"))]
        rules = line[start + 1 : -1].split(",")
        wfs[name] = Workflow(name, rules)

    ps = [
        Part(*(int(p[p.index("=") + 1 :]) for p in part.strip("{}").split(",")))
        for part in parts.split("\n")
    ]

    return wfs, ps


def part1(data: tuple[dict[str, Workflow], list[Part]]) -> int:
    workflows, parts = data
    score = 0

    in_ = workflows["in"]
    for part in parts:
        rule = in_(part)
        while rule not in {"R", "A"}:
            wf = workflows[rule]
            rule = wf(part)

        if rule == "A":
            score += part.x + part.m + part.a + part.s

    return score


def part2(data: tuple[dict[str, Workflow], list[Part]]) -> int:
    def solve(rule: str, x: range, m: range, a: range, s: range):
        if rule == "R":
            # we gain no new information
            return 0
        if rule == "A":
            # all products of remaining ranges are accepted
            return len(x) * len(m) * len(a) * len(s)

        wf = workflows[rule]
        n = 0
        for rule in wf.rules:
            # if-then rule
            if ":" in rule:
                r = rule[: (then := rule.index(":"))]
                less_than = r[1] == "<"
                value = int(r[2:then])
                target = rule[then + 1 :]
                match r[0]:
                    # since rules can be chained, whenever we do *not* jump to another rule
                    # the opposite of the previous jump-condition holds
                    case "x":
                        if less_than:
                            n += solve(target, range(max(x.start, 1), min(x.stop, value)), m, a, s)
                            x = range(max(x.start, value), min(x.stop, N))
                        else:
                            n += solve(
                                target, range(max(x.start, value + 1), min(x.stop, N)), m, a, s
                            )
                            x = range(max(x.start, 1), min(x.stop, value + 1))
                    case "m":
                        if less_than:
                            n += solve(target, x, range(max(m.start, 1), min(m.stop, value)), a, s)
                            m = range(max(m.start, value), min(m.stop, N))
                        else:
                            n += solve(
                                target, x, range(max(m.start, value + 1), min(m.stop, N)), a, s
                            )
                            m = range(max(m.start, 1), min(m.stop, value + 1))
                    case "a":
                        if less_than:
                            n += solve(target, x, m, range(max(a.start, 1), min(a.stop, value)), s)
                            a = range(max(a.start, value), min(a.stop, N))
                        else:
                            n += solve(
                                target, x, m, range(max(a.start, value + 1), min(a.stop, N)), s
                            )
                            a = range(max(a.start, 1), min(a.stop, value + 1))
                    case "s":
                        if less_than:
                            n += solve(target, x, m, a, range(max(s.start, 1), min(s.stop, value)))
                            s = range(max(s.start, value), min(s.stop, N))
                        else:
                            n += solve(
                                target, x, m, a, range(max(s.start, value + 1), min(s.stop, N))
                            )
                            s = range(max(s.start, 1), min(s.stop, value + 1))
            # basic jump
            else:
                n += solve(rule, x, m, a, s)
        return n

    workflows, _ = data
    N = 4001
    return solve("in", x=range(1, N), m=range(1, N), a=range(1, N), s=range(1, N))


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day19.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
