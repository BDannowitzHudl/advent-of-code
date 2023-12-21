"""
--- Day 21: Step Counter ---
You manage to catch the airship right as it's dropping someone else off on their
all-expenses-paid trip to Desert Island! It even helpfully drops you off near the
gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have
enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are
at solving problems and would like your help. He needs to get his steps in for the day,
and so he'd like to know which garden plots he can reach with exactly his remaining 64
steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S),
garden plots (.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then,
he can take one step north, south, east, or west, but only onto tiles that are garden
plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O,
his second step would allow him to reach any garden plot that is one step north, south,
east, or west of any tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting
position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a
total of 6 steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use
them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is
much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the
Elf reach in exactly 64 steps?

--- Part Two ---
The Elf seems confused by your answer until he realizes his mistake: he was reading
from a list of his favorite numbers that are both perfect squares and perfect cubes,
not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats
infinitely in every direction.

So, if you were to look one additional map-width or map-height out from the edge of
the example map above, you would find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm
layout; garden plots and rocks repeat as far as you can see. The Elf still starts on
the one middle tile marked S, though - every other repeated S is replaced with
a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the
example map for different numbers of steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot
marked S on your infinite map, how many garden plots could the Elf reach in
exactly 26501365 steps?
"""
from typing import List, Dict, Tuple, Set
from pathlib import Path
from enum import Enum
import networkx as nx
from numpy.polynomial.polynomial import Polynomial
from functools import lru_cache


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)


@lru_cache(maxsize=None)
def neighbors(
    g: nx.Graph, node: Tuple[int, int], height: int, width: int
) -> Set[Direction]:
    """Return a list of the neighbors of the given node, taking into account
    the fact that the field is circular.
    """
    x, y = node
    direction_set: Set[Direction] = set()
    for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
        neighbor_x = (x + direction.value[0]) % width
        neighbor_y = (y + direction.value[1]) % height
        if g.has_edge((x, y), (neighbor_x, neighbor_y)):
            direction_set.add(direction)

    return set(direction_set)


class Field:
    def __init__(self, g: nx.Graph, height: int, width: int, part: int = 1):
        self.part = part
        self.g = g
        self.height = height
        self.width = width

    def do_steps(self, n: int) -> int:
        active_set = set(
            (node for node in self.g.nodes if self.g.nodes[node]["active"] > 0)
        )

        plen = 0
        xs = []
        ys = []
        for i in range(1, n):
            new_active_set = set()
            for node in active_set:
                graph_x, graph_y = node[0] % self.width, node[1] % self.height
                direction_set = neighbors(
                    self.g, (graph_x, graph_y), self.height, self.width
                )
                for direction in direction_set:
                    neighbor_x = node[0] + direction.value[0]
                    neighbor_y = node[1] + direction.value[1]
                    new_active_set.add((neighbor_x, neighbor_y))
            active_set = new_active_set
            # if self.part == 2:
            #    if i % self.width == n % self.width:
            #        xs.append(i)
            #        ys.append(len(active_set))
            #        print(i, len(active_set), len(active_set) - plen, i // self.width)
            #        plen = len(active_set)
            #    if len(xs) > 2:
            #        poly = Polynomial.fit(xs, ys, 2)
            #        return poly(n)

        return len(active_set)


def make_field(data: List[str], part: int = 1) -> nx.Graph:
    g = nx.Graph()
    height, width = len(data), len(data[0])
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == ".":
                g.add_node((x, y), garden=True, active=0)
            elif col == "S":
                g.add_node((x, y), garden=True, active=1)
            elif col == "#":
                g.add_node((x, y), garden=False, active=0)
            else:
                raise ValueError(f"Unknown character {col} in data")
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if (x, y) in g.nodes:
                if g.nodes[(x, y)]["garden"] is True:
                    # Add edges for any node rook-adjacent to this one
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_x, new_y = x + dx, y + dy
                        if part == 2:
                            # circular boundary conditions
                            if new_x < 0:
                                new_x += width
                            elif new_x >= width:
                                new_x -= width
                            if new_y < 0:
                                new_y += height
                            elif new_y >= height:
                                new_y -= height
                        if (new_x, new_y) in g.nodes and g.nodes[(new_x, new_y)][
                            "garden"
                        ] is True:
                            g.add_edge((x, y), (new_x, new_y))
    field = Field(g=g, height=height, width=width, part=part)
    return field


def plot_field(g: nx.Graph) -> None:
    """Print out the field in ascii format, with active nodes marked with an O,
    non-active gardens with a '.', and rocks with a '#'.
    """
    x_min = min([node[0] for node in g.nodes])
    x_max = max([node[0] for node in g.nodes])
    y_min = min([node[1] for node in g.nodes])
    y_max = max([node[1] for node in g.nodes])
    for y in range(y_min, y_max + 1):
        row = ""
        for x in range(x_min, x_max + 1):
            if (x, y) in g.nodes:
                if g.nodes[(x, y)]["garden"] is True:
                    if g.nodes[(x, y)]["active"] > 0:
                        row += "O"
                    else:
                        row += "."
                else:
                    row += "#"
            else:
                row += " "
        print(row)
    print()


def part_one(data: List[str], steps: int = 6) -> int:
    field = make_field(data)
    score = field.do_steps(steps)
    return score


def part_two(data: List[str], steps: int = 6) -> int:
    field = make_field(data, part=2)
    score = field.do_steps(steps)
    return score


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "...........",
        ".....###.#.",
        ".###.##..#.",
        "..#.#...#..",
        "....#.#....",
        ".##..S####.",
        ".##..#...#.",
        ".......##..",
        ".##.#.####.",
        ".##..##.##.",
        "...........",
    ]

    # Starting Part One at 5:50AM CST

    PART_ONE_EXPECTED_VALUE: int = 16
    print(
        f"Part One: {part_one(data=TEST_DATA, steps=6)} "
        f"(expected {PART_ONE_EXPECTED_VALUE})"
    )
    print(f"Part One: {part_one(data=DATA, steps=64)}")

    # Completed Part One at 6:12AM CST

    # Starting Part Two at 6:17AM CST

    PART_TWO_EXPECTED_VALUE: Dict[int, int] = {
        6: 16,
        10: 50,
        50: 1594,
        100: 6536,
        500: 167004,
        1000: 668697,
        #    5000: 16733044,
    }
    GOAL_STEPS = 26501365
    # for steps, expected_value in PART_TWO_EXPECTED_VALUE.items():
    # print(
    #    f"Part Two Test ({steps} steps): {part_two(data=TEST_DATA, steps=steps)} "
    #    f"(expected {expected_value})"
    # )
    print(f"Part Two: {part_two(data=DATA, steps=GOAL_STEPS)}")

    # Completed Part Two at
