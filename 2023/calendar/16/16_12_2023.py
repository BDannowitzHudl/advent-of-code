"""
--- Day 16: The Floor Will Be Lava ---
With the beam of light completely focused somewhere, the reindeer leads you deeper still
into the Lava Production Facility. At some point, you realize that the steel facility walls
have been replaced with cave, and the doorways are just cave, and the floor is cave, and
you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light
in a cavern up ahead. There, you discover that the beam of light you so carefully
focused is emerging from the cavern wall closest to the facility and pouring all of
its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square
grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each
tile on the grid converts some of the beam's light into heat to melt the rock in the
cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then,
its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending
on the angle of the mirror. For instance, a rightward-moving beam that encounters
a / mirror would continue upward in the mirror's column, while a rightward-moving
beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through
the splitter as if the splitter were empty space. For instance, a rightward-moving
beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into
two beams going in each of the two directions the splitter's pointy ends are pointing.
For instance, a rightward-moving beam that encounters a | splitter would split into
two beams: one that continues upward from the splitter's column and one that
continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through
it at the same time. A tile is energized if that tile has at least one beam pass
through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams.
If a tile contains beams moving in multiple directions, the number of distinct
directions is shown instead. Here is the same diagram but instead only showing
whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption,
you need to start by analyzing the current situation. With the beam starting in
the top-left heading right, how many tiles end up being energized?

--- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt and
leads you to a nearby control panel. There, a collection of buttons lets you
align the contraption so that the beam enters from any edge tile and heading
away from that edge. (You can choose either of two directions for the beam if
it starts on a corner; for instance, if the beam starts in the bottom-right
corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any
tile in the bottom row (heading upward), any tile in the leftmost column
(heading right), or any tile in the rightmost column (heading left). To
produce lava, you need to find the configuration that energizes as many
tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth
tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest
number of tiles; how many tiles are energized in that configuration?
"""
from typing import List, Set
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class BeamDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tile:
    def __init__(self, char: str):
        self.char = char
        self.energized: bool = False
        self.history: Set[BeamDirection] = set()

    def hit(self, beam_direction: BeamDirection) -> List[BeamDirection]:
        self.energized = True
        if beam_direction in self.history:
            return []
        else:
            self.history.add(beam_direction)
        if self.char == ".":
            return [beam_direction]
        elif self.char == "/":
            if beam_direction == BeamDirection.UP:
                return [BeamDirection.RIGHT]
            elif beam_direction == BeamDirection.DOWN:
                return [BeamDirection.LEFT]
            elif beam_direction == BeamDirection.LEFT:
                return [BeamDirection.DOWN]
            elif beam_direction == BeamDirection.RIGHT:
                return [BeamDirection.UP]
        elif self.char == "\\":
            if beam_direction == BeamDirection.UP:
                return [BeamDirection.LEFT]
            elif beam_direction == BeamDirection.DOWN:
                return [BeamDirection.RIGHT]
            elif beam_direction == BeamDirection.LEFT:
                return [BeamDirection.UP]
            elif beam_direction == BeamDirection.RIGHT:
                return [BeamDirection.DOWN]
        elif self.char == "|":
            if beam_direction == BeamDirection.UP:
                return [BeamDirection.UP]
            elif beam_direction == BeamDirection.DOWN:
                return [BeamDirection.DOWN]
            elif beam_direction == BeamDirection.LEFT:
                return [BeamDirection.UP, BeamDirection.DOWN]
            elif beam_direction == BeamDirection.RIGHT:
                return [BeamDirection.UP, BeamDirection.DOWN]
        elif self.char == "-":
            if beam_direction == BeamDirection.UP:
                return [BeamDirection.LEFT, BeamDirection.RIGHT]
            elif beam_direction == BeamDirection.DOWN:
                return [BeamDirection.LEFT, BeamDirection.RIGHT]
            elif beam_direction == BeamDirection.LEFT:
                return [BeamDirection.LEFT]
            elif beam_direction == BeamDirection.RIGHT:
                return [BeamDirection.RIGHT]
        else:
            raise ValueError(f"Unknown tile character: {self.char}")


@dataclass
class WaveFront:
    direction: BeamDirection = BeamDirection.RIGHT
    x: int = 0
    y: int = 0

    def __eq__(self, other):
        return (
            self.direction == other.direction
            and self.x == other.x
            and self.y == other.y
        )

    def __hash__(self):
        return hash((self.direction, self.x, self.y))


class Grid:
    def __init__(self, data: List[str]):
        self.grid: List[List[Tile]] = []
        self.height: int = len(data)
        self.width: int = len(data[0])
        for row in data:
            self.grid.append([Tile(char) for char in row])

    def fire(
        self, wave_front: WaveFront = WaveFront(BeamDirection.RIGHT, 0, 0)
    ) -> None:
        wave_fronts = [wave_front]
        i = 0
        while wave_fronts:
            out_wave_fronts: List[WaveFront] = []
            for wave_front in wave_fronts:
                tile = self.grid[wave_front.y][wave_front.x]
                out_directions = tile.hit(wave_front.direction)
                for out_direction in out_directions:
                    if out_direction == BeamDirection.UP and wave_front.y > 0:
                        out_wave_fronts.append(
                            WaveFront(out_direction, wave_front.x, wave_front.y - 1)
                        )
                    elif (
                        out_direction == BeamDirection.DOWN
                        and wave_front.y < self.height - 1
                    ):
                        out_wave_fronts.append(
                            WaveFront(out_direction, wave_front.x, wave_front.y + 1)
                        )
                    elif out_direction == BeamDirection.LEFT and wave_front.x > 0:
                        out_wave_fronts.append(
                            WaveFront(out_direction, wave_front.x - 1, wave_front.y)
                        )
                    elif (
                        out_direction == BeamDirection.RIGHT
                        and wave_front.x < self.width - 1
                    ):
                        out_wave_fronts.append(
                            WaveFront(out_direction, wave_front.x + 1, wave_front.y)
                        )
            wave_fronts = out_wave_fronts
            wave_fronts = list(set(wave_fronts))

    def score(self) -> int:
        return sum(
            [sum([1 if tile.energized else 0 for tile in row]) for row in self.grid]
        )

    def reset(self) -> None:
        for row in self.grid:
            for tile in row:
                tile.energized = False
                tile.history = set()

    def scan(self) -> int:
        self.reset()
        top_score: int = 0
        # Scan the left and right sides
        for y in range(self.height):
            wave_front = WaveFront(BeamDirection.RIGHT, 0, y)
            self.fire(wave_front)
            top_score = max(top_score, self.score())
            self.reset()
            wave_front = WaveFront(BeamDirection.LEFT, self.width - 1, y)
            self.fire(wave_front)
            top_score = max(top_score, self.score())
            self.reset()
        # Scan the top and bottom sides
        for x in range(self.width):
            wave_front = WaveFront(BeamDirection.DOWN, x, 0)
            self.fire(wave_front)
            top_score = max(top_score, self.score())
            self.reset()
            wave_front = WaveFront(BeamDirection.UP, x, self.height - 1)
            self.fire(wave_front)
            top_score = max(top_score, self.score())
            self.reset()
        return top_score


def part_one(data: List[str]) -> int:
    grid = Grid(data)
    grid.fire()
    return grid.score()


def part_two(data: List[str]) -> int:
    grid = Grid(data)
    score = grid.scan()
    return score


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        ".|...\\....",
        "|.-.\\.....",
        ".....|-...",
        "........|.",
        "..........",
        ".........\\",
        "..../.\\\\..",
        ".-.-/..|..",
        ".|....-|.\\",
        "..//.|....",
    ]

    # Starting Part One at

    PART_ONE_EXPECTED_VALUE: int = 46
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 10:05AM CST

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 51
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
