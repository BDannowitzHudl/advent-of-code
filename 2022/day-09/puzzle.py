"""Day 9, 2022 Advent of Code puzzle solution.

Problem: https://adventofcode.com/2022/day/9
"""
from enum import Enum
from typing import Dict, List, Set
import math


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


def sign(x: int) -> int:
    """Return the sign of a number."""
    return int(math.copysign(1, x))


class Rope:
    def __init__(self, knots: int):
        """Create a rope of a certain number of Planck knots.
        Initialize all knots at the origin.
        """
        self.knots: Dict[int, List[int]] = {i: [0, 0] for i in range(knots)}
        self.tail_history: Set[List[int]] = set()

    @property
    def n_knots(self) -> int:
        return len(self.knots)

    @property
    def head(self) -> List[int]:
        return self.knots[0]

    @property
    def tail(self) -> List[int]:
        return self.knots[self.n_knots - 1]

    def move(self, direction: Direction, distance: int):
        """One row of the instructions tells us to move the head in
        one direction a certain number of times. Break this down into
        individual moves in that one direction."""
        for _ in range(distance):
            self.move_one(direction)

    def move_one(self, direction: Direction):
        """Move the head and then resolve the rest of the rope.

        At the end, log the position of the tail in the history set.
        """
        if direction == Direction.UP:
            self.head[1] += 1
        elif direction == Direction.DOWN:
            self.head[1] -= 1
        elif direction == Direction.LEFT:
            self.head[0] -= 1
        elif direction == Direction.RIGHT:
            self.head[0] += 1
        else:
            raise ValueError(f"Unknown direction: {direction}")

        for i, j in zip(range(self.n_knots - 1), range(1, self.n_knots)):
            self.resolve_move(i, j)
        self.tail_history.add(str(self.tail))

    def resolve_move(self, knot_ix_1, knot_ix_2):
        """One knot cannot be more than one queen adjacent space away from the other.

        If it is, move it to the closest queen adjacent space.
        """
        k1 = self.knots[knot_ix_1]
        k2 = self.knots[knot_ix_2]
        delta: List[int] = [
            k1[0] - k2[0],
            k1[1] - k2[1],
        ]

        # The knot is inline, but two spaces away horizontally
        if abs(delta[0]) > 1 and delta[1] == 0:
            k2[0] += sign(delta[0])
        # The knot is inline, but two spaces away vertically
        elif delta[0] == 0 and abs(delta[1]) > 1:
            k2[1] += sign(delta[1])
        # The knot is two spaces away (one queen, one rook)
        elif abs(delta[0]) > 1 or abs(delta[1]) > 1:
            k2[0] += sign(delta[0])
            k2[1] += sign(delta[1])
        # Otherwise, do nothing!
        else:
            pass


def main(data_file: str):
    with open(data_file, "r") as f:
        data = f.read().splitlines()

    rope = Rope(knots=2)
    for line in data:
        direction = Direction(line.split(" ")[0])
        distance = int(line.split(" ")[1])
        rope.move(direction, distance)

    print(f"Part 1: {len(rope.tail_history)}")

    rope = Rope(knots=10)
    for line in data:
        direction = Direction(line.split(" ")[0])
        distance = int(line.split(" ")[1])
        rope.move(direction, distance)

    print(f"Part 2: {len(rope.tail_history)}")


if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
