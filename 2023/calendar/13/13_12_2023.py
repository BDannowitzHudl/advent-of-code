"""
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which launches you
neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains
scattered around. After a while, you make your way to a nearby cluster of mountains
only to discover that the valley between them is completely full of large mirrors.
Most of the mirrors seem to be aligned in a consistent way; perhaps you should head
in that direction?

As you move through the valley of mirrors, you find that several of them have fallen
from the large metal frames keeping them in place. The mirrors are extremely flat and
shiny, and many of the fallen mirrors have lodged into the ash at strange angles.
Because the terrain is all one color, it's hard to tell where it's safe to walk or
where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your
puzzle input); perhaps by carefully analyzing these patterns, you can figure out
where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across
either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns;
arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6.
Because the vertical line is not perfectly in the middle of the pattern, part of the
pattern (column 1) has nowhere to reflect onto and can be ignored; every other column
has a reflected column within the pattern and must match exactly: column 2 matches
column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would
reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't
need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches
row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each
vertical line of reflection; to that, also add 100 multiplied by the number of rows
above each horizontal line of reflection. In the above example, the first pattern's
vertical line has 5 columns to its left and the second pattern's horizontal line has
4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you
get after summarizing all of your notes?

--- Part Two ---
You resume walking through the valley of mirrors and - SMACK! - run directly into one.
Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: exactly
one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different
reflection line to be valid. (The old reflection line won't necessarily continue being
valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
The first pattern's smudge is in the top-left corner. If the top-left # were instead .,
it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection
between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be
ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches
row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2
from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In
this example, the first pattern's new horizontal line has 3 rows above it and the
second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection. What number
do you get after summarizing the new reflection line in each pattern in your notes?
"""
from typing import List, Optional
from pathlib import Path
import numpy as np


class LavaField:
    def __init__(self, data: List[str], part: int = 1) -> None:
        self.part = part
        self.data = self._digitize(data)
        self.height = self.data.shape[0]
        self.width = self.data.shape[1]
        self.horizontal_mirror: Optional[int] = self._find_horizontal_mirror()
        self.vertical_mirror: Optional[int] = self._find_vertical_mirror()
        self.smudged_horizontal_mirror: Optional[
            int
        ] = self._find_smudged_horizontal_mirror()
        self.smudged_vertical_mirror: Optional[
            int
        ] = self._find_smudged_vertical_mirror()

        if not self.horizontal_mirror and not self.vertical_mirror:
            raise ValueError("No mirror found")
        self.score: int = self._calculate_score(part=self.part)

    def _digitize(self, data: List[str]) -> np.ndarray:
        return np.array([[1 if c == "#" else 0 for c in line] for line in data])

    def _find_horizontal_mirror(self) -> Optional[int]:
        # Scan through for candidates
        # A candidate is a row that is the same as the row below it
        for row_ix in range(1, self.height):
            chunk_size = min(row_ix, self.height - row_ix)
            if np.array_equal(
                self.data[row_ix - chunk_size : row_ix, :],
                self.data[row_ix : row_ix + chunk_size, :][::-1, :],
            ):
                return row_ix

        return None

    def _find_vertical_mirror(self) -> Optional[int]:
        for col_ix in range(1, self.width):
            chunk_size = min(col_ix, self.width - col_ix)
            if np.array_equal(
                self.data[:, col_ix - chunk_size : col_ix],
                self.data[:, col_ix : col_ix + chunk_size][:, ::-1],
            ):
                return col_ix
        return None

    def _find_smudged_horizontal_mirror(self) -> Optional[int]:
        # Scan through for candidates
        # A candidate is a row that is the same as the row below it
        for row_ix in range(1, self.height):
            chunk_size = min(row_ix, self.height - row_ix)
            top = self.data[row_ix - chunk_size : row_ix, :]
            bottom = self.data[row_ix : row_ix + chunk_size, :][::-1, :]
            diff = np.abs(top - bottom)
            if np.sum(diff) == 1:
                return row_ix

        return None

    def _find_smudged_vertical_mirror(self) -> Optional[int]:
        for col_ix in range(1, self.width):
            chunk_size = min(col_ix, self.width - col_ix)
            left = self.data[:, col_ix - chunk_size : col_ix]
            right = self.data[:, col_ix : col_ix + chunk_size][:, ::-1]
            diff = np.abs(left - right)
            if np.sum(diff) == 1:
                return col_ix
        return None

    def _calculate_score(self, part: int = 1) -> int:
        score = 0
        if part == 1:
            if self.horizontal_mirror:
                score += self.horizontal_mirror * 100
            if self.vertical_mirror:
                score += self.vertical_mirror
        elif part == 2:
            if self.smudged_horizontal_mirror:
                score += self.smudged_horizontal_mirror * 100
            if self.smudged_vertical_mirror:
                score += self.smudged_vertical_mirror
        else:
            raise ValueError("Invalid part")
        return score


def part_one(data: List[str]) -> int:
    lavafields: List[LavaField] = []
    lavafield_lines: List[str] = []
    for line in data:
        if line != "":
            lavafield_lines.append(line)
        else:
            lf = LavaField(lavafield_lines)
            lavafields.append(lf)
            lavafield_lines = []
    if lavafield_lines:
        lavafields.append(LavaField(lavafield_lines))
    score = sum([lf.score for lf in lavafields])
    return score


def part_two(data: List[str]) -> int:
    lavafields: List[LavaField] = []
    lavafield_lines: List[str] = []
    for line in data:
        if line != "":
            lavafield_lines.append(line)
        else:
            lf = LavaField(lavafield_lines, part=2)
            lavafields.append(lf)
            lavafield_lines = []
    if lavafield_lines:
        lavafields.append(LavaField(lavafield_lines, part=2))
    score = sum([lf.score for lf in lavafields])
    return score


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
        "",
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]

    # Starting Part One at

    PART_ONE_EXPECTED_VALUE: int = 405
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at 10:38AM CST

    PART_TWO_EXPECTED_VALUE: int = 400
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
