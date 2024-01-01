"""
--- Day 24: Never Tell Me The Odds ---
It seems like something is going wrong with the snow-making process. Instead of
forming snow, the water that's been absorbed into the air seems to be forming hail!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air
in perfectly linear trajectories. You make a note of each hailstone's position and
velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The
positions indicate where the hailstones are right now (at time 0). The velocities are
constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone
specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z
position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond,
the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with
each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward
in time, how many of the hailstones' paths will intersect within a test area? (The
hailstones themselves don't have to collide, just test for intersections between the
paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at
least 7 and at most 27; in your actual data, you'll need to check a much larger test
area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the
test area.

However, you'll need to search a much larger test area if you want to see if any
hailstones might collide. Look for intersections that happen with an X and Y position
each at least 200000000000000 and at most 400000000000000. Disregard the Z axis
entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for
intersections. How many of these intersections occur within the test area?

--- Part Two ---
Upon further analysis, it doesn't seem like any hailstones will naturally collide.
It's up to you to fix that!

You find a rock on the ground nearby. While it seems extremely unlikely, if you throw
it just right, you should be able to hit every hailstone in a single throw!

You can use the probably-magical winds to reach any integer position you like and to
propel the rock at any integer velocity. Now including the Z axis in your calculations,
if you throw the rock at time 0, where do you need to be so that the rock perfectly
collides with every hailstone? Due to probably-magical inertia, the rock won't slow
down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position 24, 13, 10 and
throwing the rock at velocity -3, 1, 2. If you do this, you will hit every hailstone
as follows:

Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
Above, each hailstone is identified by its initial position and its velocity. Then,
the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has exactly the same position as one of the hailstones,
obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds
after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10.
Adding these three coordinates together produces 47. (Don't add any coordinates from
the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time 0 so that it
perfectly collides with every hailstone. What do you get if you add up the X, Y, and Z
coordinates of that initial position?
"""
from typing import List
from pathlib import Path
from itertools import combinations
import math
from tqdm import tqdm


def calculate_time_of_collision(particle1, particle2):
    """Calculates the time of collision between two particles, ensuring a positive collision time."""

    dx = particle2.x - particle1.x
    dy = particle2.y - particle1.y
    dz = particle2.z - particle1.z
    dvx = particle2.vx - particle1.vx
    dvy = particle2.vy - particle1.vy
    dvz = particle2.vz - particle1.vz

    a = dvx**2 + dvy**2 + dvz**2
    b = 2 * (dx * dvx + dy * dvy + dz * dvz)
    c = dx**2 + dy**2 + dz**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None  # No collision

    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    # Choose the positive collision time
    collision_time = t1 if t1 > 0 else t2
    return collision_time


def branch_and_bound(particles, bounds):
    """Recursively explores the search space using branch and bound."""

    # Check if current bounds represent a single point
    if all(bound[0] == bound[1] for bound in bounds):
        initial_position, initial_velocity = zip(*bounds)
        return initial_position, initial_velocity

    best_solution = None
    for dimension in range(6):  # Iterate through x, y, z, vx, vy, vz
        mid = (bounds[dimension][0] + bounds[dimension][1]) // 2

        # Explore left branch
        left_bounds = bounds.copy()
        left_bounds[dimension] = (bounds[dimension][0], mid)
        solution = branch_and_bound(particles, left_bounds)
        if solution:
            best_solution = solution
            break

        # Explore right branch (if needed)
        right_bounds = bounds.copy()
        right_bounds[dimension] = (mid + 1, bounds[dimension][1])
        solution = branch_and_bound(particles, right_bounds)
        if solution:
            best_solution = solution

    return best_solution


class Hailstone:
    def __init__(self, x: int, y: int, z: int, vx: int, vy: int, vz: int):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.m, self.b = self._get_line()
        self.m_xz, self.b_xz = self._get_line_xz()

    def _get_line(self) -> List[float]:
        m = self.vy / self.vx if self.vx != 0 else math.inf
        b = self.y - m * self.x
        return m, b

    def _get_line_xz(self) -> List[float]:
        m = self.vz / self.vx if self.vx != 0 else math.inf
        b = self.z - m * self.x
        return m, b

    @property
    def _position(self) -> List[int]:
        return [self.x, self.y, self.z]

    @property
    def _velocity(self) -> List[int]:
        return [self.vx, self.vy, self.vz]

    @classmethod
    def from_position_velocity(
        cls, position: List[int], velocity: List[int]
    ) -> "Hailstone":
        x, y, z = position
        vx, vy, vz = velocity
        return cls(x, y, z, vx, vy, vz)

    def __repr__(self) -> str:
        return f"{self._position} @ {self._velocity}"

    def __str__(self) -> str:
        return f"{self._position} @ {self._velocity}"

    def coincident(self, other: "Hailstone") -> bool:
        """Test if the two are coincident in x-y space."""
        if self.m != other.m:
            return False
        if self.b != other.b:
            return False
        return True

    def intersects(
        self,
        other: "Hailstone",
        xy_min: int = 200_000_000_000_000,
        xy_max: int = 400_000_000_000_000,
    ) -> bool:
        if self.m == other.m:
            if self.coincident(other):
                return True
            return False
        x = (other.b - self.b) / (self.m - other.m)
        y = self.m * x + self.b
        t1 = (
            (x - self.x) / self.vx
            if self.vx != 0
            else (y - self.y) / self.vy
            if self.vy != 0
            else 0
        )
        t2 = (
            (x - other.x) / other.vx
            if other.vx != 0
            else (y - other.y) / other.vy
            if other.vy != 0
            else 0
        )
        if t1 < 0 or t2 < 0:
            return False
        if x < xy_min or x > xy_max or y < xy_min or y > xy_max:
            return False
        return True

    def intersects_xy(
        self,
        other: "Hailstone",
        xy_min: int = 200_000_000_000_000,
        xy_max: int = 400_000_000_000_000,
    ) -> bool:
        if self.m == other.m:
            if self.coincident(other):
                return True
            return False
        x = (other.b - self.b) / (self.m - other.m)
        y = self.m * x + self.b
        t1 = (
            (x - self.x) / self.vx
            if self.vx != 0
            else (y - self.y) / self.vy
            if self.vy != 0
            else 0
        )
        t2 = (
            (x - other.x) / other.vx
            if other.vx != 0
            else (y - other.y) / other.vy
            if other.vy != 0
            else 0
        )
        if t1 < 0 or t2 < 0:
            return False
        if x < xy_min or x > xy_max or y < xy_min or y > xy_max:
            return False
        return True

    def intersects_xz(
        self,
        other: "Hailstone",
        xy_min: int = 200_000_000_000_000,
        xy_max: int = 400_000_000_000_000,
    ) -> bool:
        if self.m_xz == other.m_xz:
            if self.b_xz == other.b_xz:
                return True
            return False
        x = (other.b_xz - self.b_xz) / (self.m_xz - other.m_xz)
        z = self.m_xz * x + self.b_xz
        t1 = (
            (x - self.x) / self.vx
            if self.vx != 0
            else (z - self.z) / self.vz
            if self.vz != 0
            else 0
        )
        t2 = (
            (x - other.x) / other.vx
            if other.vx != 0
            else (z - other.z) / other.vz
            if other.vz != 0
            else 0
        )
        if t1 < 0 or t2 < 0:
            return False
        if x < xy_min or x > xy_max or z < xy_min or z > xy_max:
            return False
        return True

    def shift(self, velocity: List[int]) -> "Hailstone":
        return Hailstone.from_position_velocity(
            position=self._position,
            velocity=[v - dv for v, dv in zip(self._velocity, velocity)],
        )


class HailStorm:
    def __init__(self, hailstones: List[Hailstone], min_val: int, max_val: int):
        self.hailstones = hailstones
        self.min_val = min_val
        self.max_val = max_val

    def intersects(self, velocity: List[int]) -> bool:
        for hailstone_a, hailstone_b in combinations(self.hailstones, 2):
            hailstone_a_shifted = hailstone_a.shift(velocity)
            hailstone_b_shifted = hailstone_b.shift(velocity)
            if not hailstone_a_shifted.intersects_xy(
                hailstone_b_shifted, self.min_val, self.max_val
            ):
                return False

        # So, they all cross in the x-y plane, but do they all share a common z?
        for hailstone_a, hailstone_b in combinations(self.hailstones, 2):
            hailstone_a_shifted = hailstone_a.shift(velocity)
            hailstone_b_shifted = hailstone_b.shift(velocity)
            if not hailstone_a_shifted.intersects_xz(
                hailstone_b_shifted, self.min_val, self.max_val
            ):
                return False

        return True

    def scan_velocity_range(self, velocity_range: range) -> List[int]:
        for vx in tqdm(velocity_range, total=len(velocity_range)):
            for vy in velocity_range:
                for vz in velocity_range:
                    if self.intersects([vx, vy, vz]):
                        return [vx, vy, vz]


def part_one(
    data: List[str],
    xy_min: int = 200_000_000_000_000,
    xy_max: int = 400_000_000_000_000,
) -> int:
    hailstones = []
    for line in data:
        position, velocity = line.split(" @ ")
        position = [int(x) for x in position.split(", ")]
        velocity = [int(x) for x in velocity.split(", ")]
        hailstones.append(
            Hailstone.from_position_velocity(
                position=position,
                velocity=velocity,
            )
        )
    collisions = 0
    for hailstone_a, hailstone_b in combinations(hailstones, 2):
        if hailstone_a.intersects(hailstone_b, xy_min, xy_max):
            collisions += 1
    return collisions


def intersection_point(hailstone_a: Hailstone, hailstone_b: Hailstone) -> List[int]:
    if hailstone_a.m == hailstone_b.m:
        return hailstone_a._position
    x = (hailstone_b.b - hailstone_a.b) / (hailstone_a.m - hailstone_b.m)
    y = hailstone_a.m * x + hailstone_a.b
    z = hailstone_a.m_xz * x + hailstone_a.b_xz
    return [int(round(x)), int(round(y)), int(round(z))]


def part_two(
    data: List[str],
    xy_min: int = 200_000_000_000_000,
    xy_max: int = 400_000_000_000_000,
    velocity_range: range = range(-100, 100),
):
    hailstones = []
    for line in data:
        position, velocity = line.split(" @ ")
        position = [int(x) for x in position.split(", ")]
        velocity = [int(x) for x in velocity.split(", ")]
        hailstones.append(
            Hailstone.from_position_velocity(
                position=position,
                velocity=velocity,
            )
        )

    some_hailstones = hailstones[:5]
    hailstorm = HailStorm(some_hailstones, xy_min, xy_max)
    velocity = hailstorm.scan_velocity_range(velocity_range)
    position = intersection_point(
        hailstones[0].shift(velocity), hailstones[1].shift(velocity)
    )
    print(velocity, position)
    return int(round(sum(position)))


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()
    TEST_DATA = (
        open(WORKING_DIR / "test_data.csv", encoding="utf-8").read().splitlines()
    )

    # Starting Part One at

    PART_ONE_EXPECTED_VALUE: int = 2
    # print(
    #     f"Part One: {part_one(TEST_DATA, xy_min=7, xy_max=27)} "
    #     f"(expected {PART_ONE_EXPECTED_VALUE})"
    # )
    # print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 47
    print(
        "Part Two: "
        f"{part_two(TEST_DATA, xy_min=7, xy_max=27, velocity_range=range(-3, 3))} "
        f"(expected {PART_TWO_EXPECTED_VALUE})"
    )
    print("Part Two: " f"{part_two(DATA, velocity_range=range(-10_000, 10_000))}")

    # Completed Part Two at
