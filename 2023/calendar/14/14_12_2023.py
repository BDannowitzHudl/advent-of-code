"""
--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive parabolic
reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly
in the shape of a parabolic reflector dish, each individual mirror seems to be pointing
in slightly the wrong direction. If the dish is meant to focus light, all it's doing
right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector
dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an
elaborate system of ropes and pulleys to a large metal platform below the dish. The
platform is covered in large rocks of various shapes. Depending on their position, the
weight of the rocks deforms the platform, and the shape of the platform controls which
ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a
control panel on the side that lets you tilt it in one of four directions! The rounded
rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will
stay in place. You note the positions of all of the empty spaces (.) and rocks (your
puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to
ensure the platform doesn't collapse, you should calculate the total load on the north
support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows
from the rock to the south edge of the platform, including the row the rock is on.
(Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by
each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this
example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the
total load on the north support beams?

--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do
that, you'll need to move the rocks to the edges of the platform. Fortunately, a button
on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then
west, then south, then east. After each tilt, the rounded rocks roll as far as they can
before the platform tilts in the next direction. After one cycle, the platform will
have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried
about the north support beams. To make sure they'll survive for a while, you need to
calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support
beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the
north support beams?
"""
from typing import List
from pathlib import Path
from enum import Enum
import functools
from tqdm import tqdm


class PlatformObject(Enum):
    EMPTY = "."
    CUBE = "#"
    ROUND = "O"


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Platform:
    def __init__(self, data: List[str]) -> None:
        self.data = data
        self.width = len(data[0])
        self.height = len(data)
        self.platform = self._create_platform()

    def _create_platform(self) -> List[List[int]]:
        return [[PlatformObject(char) for char in row] for row in self.data]

    def __repr__(self) -> str:
        repr_str = ""
        for row in self.platform:
            repr_str += "".join([obj.value for obj in row]) + "\n"
        return repr_str

    def __str__(self) -> str:
        return self.__repr__()

    def tilt(self, direction: Direction) -> None:
        if direction == Direction.NORTH:
            self._tilt_north()
        elif direction == Direction.SOUTH:
            self._tilt_south()
        elif direction == Direction.EAST:
            self._tilt_east()
        elif direction == Direction.WEST:
            self._tilt_west()

    def cycle(self, n: int = 1) -> None:
        for _ in range(n):
            self.tilt(Direction.NORTH)
            self.tilt(Direction.WEST)
            self.tilt(Direction.SOUTH)
            self.tilt(Direction.EAST)

    def occupied(self, row: int, col: int) -> bool:
        if self.platform[row][col] != PlatformObject.EMPTY:
            return True
        return False

    def _tilt_north(self) -> None:
        for row in range(1, self.height):
            for col in range(self.width):
                if self.platform[row][col] == PlatformObject.ROUND:
                    check_rows = list(range(row))[::-1]
                    min_row = row
                    for check_row in check_rows:
                        if not self.occupied(check_row, col):
                            min_row = check_row
                        else:
                            break
                    if min_row != row:
                        self.platform[min_row][col] = PlatformObject.ROUND
                        self.platform[row][col] = PlatformObject.EMPTY

    def _tilt_south(self) -> None:
        for row in list(range(self.height - 1))[::-1]:
            for col in range(self.width):
                if self.platform[row][col] == PlatformObject.ROUND:
                    check_rows = list(range(row + 1, self.height))
                    max_row = row
                    # print(row, col, check_rows)
                    for check_row in check_rows:
                        if not self.occupied(check_row, col):
                            max_row = check_row
                        else:
                            break
                    if max_row != row:
                        self.platform[max_row][col] = PlatformObject.ROUND
                        self.platform[row][col] = PlatformObject.EMPTY

    def _tilt_east(self) -> None:
        for col in range(self.width - 1, -1, -1):
            for row in range(self.height):
                if self.platform[row][col] == PlatformObject.ROUND:
                    check_cols = list(range(col + 1, self.width))
                    max_col = col
                    for check_col in check_cols:
                        if not self.occupied(row, check_col):
                            max_col = check_col
                        else:
                            break
                    if max_col != col:
                        self.platform[row][max_col] = PlatformObject.ROUND
                        self.platform[row][col] = PlatformObject.EMPTY

    def _tilt_west(self) -> None:
        for col in range(1, self.width):
            for row in range(self.height):
                if self.platform[row][col] == PlatformObject.ROUND:
                    check_cols = list(range(col))[::-1]
                    min_col = col
                    for check_col in check_cols:
                        if not self.occupied(row, check_col):
                            min_col = check_col
                        else:
                            break
                    if min_col != col:
                        self.platform[row][min_col] = PlatformObject.ROUND
                        self.platform[row][col] = PlatformObject.EMPTY

    def _row_count(self, row: int, object_type: PlatformObject) -> int:
        return sum(
            1 for col in range(self.width) if self.platform[row][col] == object_type
        )

    def score(self) -> int:
        score: int = 0
        for row in range(self.height):
            multiplier: int = self.height - row
            score += multiplier * self._row_count(row, PlatformObject.ROUND)
        return score


@functools.lru_cache(maxsize=None)
def cycle(platform_str: str, n: int = 1) -> None:
    p = Platform(platform_str.splitlines())
    for _ in range(n):
        p.tilt(Direction.NORTH)
        p.tilt(Direction.WEST)
        p.tilt(Direction.SOUTH)
        p.tilt(Direction.EAST)
    return str(p)


def part_one(data: List[str]) -> int:
    p = Platform(data)
    p.tilt(Direction.NORTH)
    return p.score()


def part_two(data: List[str]) -> int:
    p = Platform(data)
    p_str = str(p)
    for _ in tqdm(range(10_000_000)):
        p_str = cycle(p_str, n=100)

    p = Platform(p_str.splitlines())

    return p.score()


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#....",
    ]

    # Starting Part One at 7:40AM CST

    PART_ONE_EXPECTED_VALUE: int = 136
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 64
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 9:12AM CST
