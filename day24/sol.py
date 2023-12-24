import itertools as it

from z3 import Real, Solver, sat

from timing_util import Timing

Vec3D = tuple[int, int, int] | tuple[float, float, float]
Vec2D = tuple[int, int] | tuple[float, float]


def get_data(data: str) -> list[tuple[Vec3D, Vec3D]]:
    lines = []
    for line in data.split("\n"):
        position, direction = line.split(" @ ")
        position = tuple(map(int, position.split(", ")))
        direction = tuple(map(int, direction.split(", ")))
        lines.append((position, direction))
    return lines


def intersect_vec2(a: Vec2D, a_d: Vec2D, b: Vec2D, b_d: Vec2D) -> tuple[float, float, Vec2D] | None:
    x0a, y0a = a
    dxa, dya = a_d
    x0b, y0b = b
    dxb, dyb = b_d

    d = dxa * dyb - dxb * dya
    # parallel lines
    if d == 0:
        return None
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
    s = 0
    for (a_pos, a_vel), (b_pos, b_vel) in it.combinations(data, 2):
        if nullable_intersection := intersect_vec2(a_pos[:2], a_vel[:2], b_pos[:2], b_vel[:2]):
            t, u, (x, y) = nullable_intersection
            # not in the future for first hailstone
            if t < 0:
                continue

            # not in the future for second hailstone
            if u < 0:
                continue

            # not in the specified area
            if not (x_min <= x <= x_max and y_min <= y <= y_max):
                continue

            # found one collision
            s += 1
    return s


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
