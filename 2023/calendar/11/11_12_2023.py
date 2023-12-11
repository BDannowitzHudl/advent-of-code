"""
--- Day 11: Cosmic Expansion ---
You continue following signs for "Hot Springs" and eventually come across an
observatory. The Elf within turns out to be a researcher studying cosmic expansion
using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this
research project. However, he confirms that the hot springs are the next-closest area
likely to have people; he'll even take you straight there once he's done with today's
observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant
image (your puzzle input). The image includes empty space (.) and galaxies (#). For
example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path
between every pair of galaxies. However, there's a catch: the universe expanded in
the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact,
the result is that any rows or columns that contain no galaxies should all actually be
twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion
therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of
galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the
pair doesn't matter. For each pair, find any shortest path between the two galaxies
using only steps that move up, down, left, or right exactly one . or # at a time.
(The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5
to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here
are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between
all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of
galaxies. What is the sum of these lengths?

--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially
estimated.

Now, instead of the expansion you did before, make each empty row or column one million
times larger. That is, each empty row should be replaced with 1000000 empty rows, and
each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the
sum of the shortest paths between every pair of galaxies would be 1030. If each empty
row or column were merely 100 times larger, the sum of the shortest paths between every
pair of galaxies would be 8410. However, your universe will need to expand far beyond
these values.)

Starting with the same initial image, expand the universe according to these new rules,
then find the length of the shortest path between every pair of galaxies. What is the
sum of these lengths?
"""
from typing import List
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy import sparse


def make_universe(data: List[str]) -> sparse.lil_matrix:
    # Create sparse array of universe
    arr = sparse.lil_matrix((len(data), len(data[0])), dtype=np.int8)
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == "#":
                arr[row, col] = 1
    return arr


def expand_universe(universe: sparse.lil_matrix, factor: int = 2) -> sparse.lil_matrix:
    empty_col_idx = np.where(universe.sum(axis=0) == 0)[1]
    empty_row_idx = np.where(universe.sum(axis=1) == 0)[0]
    for col in empty_col_idx[::-1]:
        # Insert a new empty column after each empty column
        universe = sparse.hstack(
            [
                universe[:, : col + 1],
                sparse.lil_matrix((universe.shape[0], factor - 1)),
                universe[:, col + 1 :],
            ],
            format="lil",
        )
    for row in empty_row_idx[::-1]:
        # Insert a new empty row after each empty row
        universe = sparse.vstack(
            [
                universe[: row + 1, :],
                sparse.lil_matrix((factor - 1, universe.shape[1])),
                universe[row + 1 :, :],
            ],
            format="lil",
        )
    return universe


def part_one(data: List[str]) -> int:
    universe = make_universe(data)
    expanded_universe = expand_universe(universe)
    rows, cols = expanded_universe.nonzero()
    coords = list(zip(rows, cols))
    combos = combinations(coords, 2)
    total_distance = 0
    for combo in combos:
        # Calculate the manhattan distance
        total_distance += sum(abs(a - b) for a, b in zip(*combo))

    return total_distance


def part_two(data: List[str], factor: int = 2) -> int:
    universe = make_universe(data)
    expanded_universe = expand_universe(universe, factor=factor)
    rows, cols = expanded_universe.nonzero()
    coords = list(zip(rows, cols))
    combos = combinations(coords, 2)
    total_distance = 0
    for combo in combos:
        # Calculate the manhattan distance
        total_distance += sum(abs(a - b) for a, b in zip(*combo))

    return total_distance


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]

    # Starting Part One at 7:35AM CST

    PART_ONE_EXPECTED_VALUE: int = 374
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 8:05AM CST

    # Starting Part Two at 8:08AM CST

    PART_TWO_EXPECTED_VALUE_10: int = 1030
    PART_TWO_EXPECTED_VALUE_100: int = 8410
    print(
        f"Part Two: {part_two(TEST_DATA, 10)} (expected {PART_TWO_EXPECTED_VALUE_10})"
    )
    print(
        f"Part Two: {part_two(TEST_DATA, 100)} (expected {PART_TWO_EXPECTED_VALUE_100})"
    )
    print(f"Part Two: {part_two(DATA, factor=1_000_000)}")

    # Completed Part Two at 8:16AM CST
