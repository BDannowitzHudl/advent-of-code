"""
--- Day 18: Lavaduct Lagoon ---
Thanks to your efforts, the machine parts factory is one of the first factories up and
running since the lavafall came back. However, to catch up with the large backlog of
parts requests, the factory will also need a large supply of lava for a while; the
Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a
look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified
number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes
as they go. The directions are given as seen from above, so if "up" were north, then
"right" would be east, and so on. Each trench is also listed with the color that the
edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop
of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just
the edge of the lagoon; the next step is to dig out the interior so that it is one
meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the
interior is dug out, the edges are also painted according to the color codes in the
dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig
plan, how many cubic meters of lava could it hold?

--- Part Two ---
The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and
instruction parameters when producing the dig plan. They don't have time to fix the
bug; one of them asks if you can extract the correct instructions from the hexadecimal
codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits
encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal
digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true
instructions:

#70c710 = R 461937
#0dc571 = D 56407
#5713f0 = R 356671
#d2c081 = D 863240
#59c680 = R 367720
#411b91 = D 266681
#8ceee2 = L 577262
#caa173 = U 829975
#1b58a2 = L 112010
#caa171 = D 829975
#7807d2 = L 491645
#a77fa3 = U 686074
#015232 = L 5411
#7a21e3 = U 500254
Digging out this loop and its interior produces a lagoon that can hold an impressive
952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow
this new dig plan, how many cubic meters of lava could the lagoon hold?


"""
from typing import List
from pathlib import Path
from shapely.geometry import Polygon, Point
from shapely import BufferCapStyle, BufferJoinStyle


class Ditch:
    def __init__(self, data: List[str], part: int = 1) -> None:
        self.part = part
        self.poly = self._create_poly(data)

    def _create_poly(self, data: List[str]) -> Polygon:
        points = [Point(0, 0)]
        for line in data:
            direction, distance, _ = self._parse_line(line)
            if direction == "R":
                points.append(Point(points[-1].x + distance, points[-1].y))
            elif direction == "L":
                points.append(Point(points[-1].x - distance, points[-1].y))
            elif direction == "U":
                points.append(Point(points[-1].x, points[-1].y + distance))
            elif direction == "D":
                points.append(Point(points[-1].x, points[-1].y - distance))
        # return to origin
        points.append(Point(0, 0))
        return Polygon(points)

    def _parse_line(self, line: str) -> tuple:
        direction_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
        if self.part == 1:
            direction, distance, color = line.split()
            distance = int(distance)
            color = color[1:-1]
        elif self.part == 2:
            _, _, hex_str = line.split()
            hex_str = hex_str[2:-1]
            direction = direction_map[hex_str[-1]]
            distance = int(hex_str[:-1], 16)
            color = "black"

        return direction, distance, color

    @property
    def area(self) -> int:
        return int(
            self.poly.buffer(
                0.5, cap_style=BufferCapStyle.square, join_style=BufferJoinStyle.mitre
            ).area
        )

    def save(self, filename: str) -> None:
        from matplotlib import pyplot as plt

        fig, ax = plt.subplots()
        x, y = self.poly.buffer(
            0.5, cap_style=BufferCapStyle.square, join_style=BufferJoinStyle.mitre
        ).exterior.xy
        ax.plot(x, y, color="#999999", linewidth=3, zorder=1)
        # Fill with lava red
        ax.fill(
            x,
            y,
            color="#FF0000",
            alpha=0.5,
            linewidth=0,
            zorder=2,
        )
        plt.savefig(filename)


def part_one(data: List[str]) -> int:
    ditch = Ditch(data)
    ditch.save("ditch.png")
    return ditch.area


def part_two(data: List[str]) -> int:
    ditch = Ditch(data, part=2)
    ditch.save("ditch2.png")
    return ditch.area


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]

    # Starting Part One at 8:58AM CST

    PART_ONE_EXPECTED_VALUE: int = 62
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 9:20AM CST

    # Starting Part Two at 9:23AM CST

    PART_TWO_EXPECTED_VALUE: int = 952408144115
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
