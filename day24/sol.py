import itertools as it

from z3 import Real, Solver, sat

from timing_util import Timing

Vec2D = tuple[float, float]
Vec3D = tuple[float, float, float]


def get_data(data: str) -> list[tuple[Vec3D, Vec3D]]:
    lines = []
    for line in data.split("\n"):
        position, direction = line.split(" @ ")
        position = tuple(map(int, position.split(", ")))
        direction = tuple(map(int, direction.split(", ")))
        lines.append((position, direction))
    return lines


def intersect_vec2(a: Vec2D, a_d: Vec2D, b: Vec2D, b_d: Vec2D) -> tuple[float, float, Vec2D] | None:
    dxa, dya = a_d
    dxb, dyb = b_d
    if (d := dxa * dyb - dxb * dya) == 0:
        return None  # parallel lines

    x0a, y0a = a
    x0b, y0b = b
    t = ((x0b - x0a) * dyb + (y0a - y0b) * dxb) / d
    u = ((x0b - x0a) * dya + (y0a - y0b) * dxa) / d

    return t, u, (x0a + dxa * t, y0a + dya * t)


def part1(
    data: list[tuple[Vec3D, Vec3D]],
    x_min: int = 200000000000000,
    y_min: int = 200000000000000,
    x_max: int = 400000000000000,
    y_max: int = 400000000000000,
) -> int:
    def has_intersection(a: Vec2D, a_d: Vec2D, b: Vec2D, b_d: Vec2D) -> bool:
        return (
            (r := intersect_vec2(a, a_d, b, b_d)) is not None
            and r[0] >= 0  # in the future for hailstone1
            and r[1] >= 0  # in the future for hailstone2
            and x_min <= r[2][0] <= x_max  # in the specified area (x)
            and y_min <= r[2][1] <= y_max  # in the specified area (y)
        )

    return sum(
        has_intersection(a[:2], a_d[:2], b[:2], b_d[:2])  # disregard z
        for (a, a_d), (b, b_d) in it.combinations(data, 2)
    )


def part2(data: list[tuple[Vec3D, Vec3D]]) -> int:
    # not even trying to do something smart here
    x, y, z, vx, vy, vz = Real("x"), Real("y"), Real("z"), Real("vx"), Real("vy"), Real("vz")
    solver = Solver()
    for i, ((hail_x, hail_y, hail_z), (hail_vx, hail_vy, hail_vz)) in enumerate(data):
        # solve for a time t such that rock.x + t * rock.vx == hail.x + t * hail.vx
        t = Real(f"t{i + 1}")
        solver.add(x + t * vx == hail_x + t * hail_vx)  # pyright: ignore[reportGeneralTypeIssues]
        solver.add(y + t * vy == hail_y + t * hail_vy)  # pyright: ignore[reportGeneralTypeIssues]
        solver.add(z + t * vz == hail_z + t * hail_vz)  # pyright: ignore[reportGeneralTypeIssues]

    if solver.check() == sat:
        model = solver.model()
        return model.eval(x + y + z).as_long()  # pyright: ignore[reportGeneralTypeIssues]
    else:
        raise ValueError("unsat")


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day24.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
