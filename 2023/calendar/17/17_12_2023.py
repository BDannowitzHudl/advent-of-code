"""
--- Day 17: Clumsy Crucible ---
The lava starts flowing rapidly once the Lava Production Facility is operational. As
you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear
Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding
anyone on your way up: half of Gear Island is empty, but the half below you is a giant
factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall.
Lavaducts will eventually carry the lava throughout the city, but to make use of it
immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become
very difficult to steer at high speeds, and so it can be hard to go in a straight
line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to
find the best way to get the crucible from the lava pool to the machine parts factory.
To do this, you need to minimize heat loss while choosing a route that doesn't require
the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns,
ambient temperature, and hundreds of other parameters to calculate exactly how much
heat loss can be expected for a crucible entering any particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if
the crucible enters that block. The starting point, the lava pool, is the top-left city
block; the destination, the machine parts factory, is the bottom-right city block.
(Because you already start in the top-left block, you don't incur that block's heat
loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for
very long, it can move at most three blocks in a single direction before it must
turn 90 degrees left or right. The crucible also can't reverse direction; after
entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
This path never moves more than three consecutive blocks in the same direction and
incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not
moving more than three consecutive blocks in the same direction, what is the least
heat loss it can incur?

--- Part Two ---
The crucibles of lava simply aren't large enough to provide an adequate supply of lava
to the machine parts factory. Instead, the Elves are going to upgrade to ultra
crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do
they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of
four blocks in that direction before it can turn (or even before it can stop at the
end). However, it will eventually start to get wobbly: an ultra crucible can move a
maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss
of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what
is the least heat loss it can incur?
"""
from typing import List, Tuple
from pathlib import Path
import numpy as np
from networkx import DiGraph
from networkx.algorithms.shortest_paths import shortest_path_length, shortest_path
from networkx.exception import NetworkXNoPath


def make_digraph(data: List[str], min_steps: int = 0, max_steps: int = 3) -> DiGraph:
    """Make a graph that represents the data

    For each cell in the grid, make 4*3 nodes, one for each direction the crucible
    could be facing times the number of consecutive steps it could be going.
    Then, connect each node to the nodes that represent the next valid steps.

    The cell values map to the weights of edges going TO the node.
    """

    dg = DiGraph()
    weights = [[int(cell) for cell in row] for row in data]
    for j, row in enumerate(data):
        for i, cell in enumerate(row):
            for direction in "NESW":
                for steps in range(1, max_steps + 1):
                    node = (i, j, direction, steps)

                    # Add an edge going north
                    if (
                        (direction in "EW" and steps >= min_steps)
                        or (direction == "N" and steps < max_steps)
                    ) and j - 1 >= 0:
                        new_steps = steps + 1 if direction == "N" else 1
                        if j - 1 >= 0:
                            dg.add_edge(
                                node,
                                (i, j - 1, "N", new_steps),
                                weight=weights[j - 1][i],
                            )
                    # Add an edge going east
                    if (
                        (direction in "NS" and steps >= min_steps)
                        or (direction == "E" and steps < max_steps)
                    ) and i + 1 < len(row):
                        new_steps = steps + 1 if direction == "E" else 1
                        dg.add_edge(
                            node,
                            (i + 1, j, "E", new_steps),
                            weight=weights[j][i + 1],
                        )
                    # Add an edge going south
                    if (
                        (direction in "EW" and steps >= min_steps)
                        or (direction == "S" and steps < max_steps)
                    ) and j + 1 < len(data):
                        new_steps = steps + 1 if direction == "S" else 1
                        dg.add_edge(
                            node,
                            (i, j + 1, "S", new_steps),
                            weight=weights[j + 1][i],
                        )
                    # Add an edge going west
                    if (
                        (direction in "NS" and steps >= min_steps)
                        or (direction == "W" and steps < max_steps)
                    ) and i - 1 >= 0:
                        new_steps = steps + 1 if direction == "W" else 1
                        dg.add_edge(
                            node,
                            (i - 1, j, "W", new_steps),
                            weight=weights[j][i - 1],
                        )
    # Add the start node
    start_node = (0, 0, "N", 1)
    # This special one connexts to (1, 0, "E", 1) and (0, 1, "S", 1)
    dg.add_edge(start_node, (1, 0, "E", 1), weight=weights[0][1])
    dg.add_edge(start_node, (0, 1, "S", 1), weight=weights[1][0])

    return dg


def get_shortest_path_length(
    dg: DiGraph,
    start: Tuple[int, int],
    end: Tuple[int, int],
    min_steps: int = 1,
    max_steps: int = 3,
) -> int:
    """Get the shortest path length going from any of the (0, 0, "N", 1) node to any of
    the (len(row) - 1, len(data) - 1, *, *) nodes where the direction is eigher E or S
    """
    return_length = np.inf
    for direction in ("E", "S"):
        for steps in range(min_steps, max_steps + 1):
            try:
                path_length = shortest_path_length(
                    dg,
                    (start[0], start[1], "N", 1),
                    (end[0], end[1], direction, steps),
                    weight="weight",
                )
                if path_length < return_length:
                    return_length = path_length
            except NetworkXNoPath:
                pass
    return return_length


def part_one(data: List[str]) -> int:
    dg = make_digraph(data)
    path_length = get_shortest_path_length(
        dg, start=(0, 0), end=(len(data) - 1, len(data[0]) - 1)
    )
    return path_length


def part_two(data: List[str]) -> int:
    dg = make_digraph(data, min_steps=4, max_steps=10)
    path_length = get_shortest_path_length(
        dg,
        start=(0, 0),
        end=(len(data[0]) - 1, len(data) - 1),
        min_steps=4,
        max_steps=10,
    )
    return path_length


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533",
    ]

    # Starting Part One at 7:20AM CST

    PART_ONE_EXPECTED_VALUE: int = 102
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 7:50AM CST

    TEST_DATA_TWO = [
        "111111111111",
        "999999999991",
        "999999999991",
        "999999999991",
        "999999999991",
    ]
    # Starting Part Two at 7:55AM CST

    PART_TWO_EXPECTED_VALUE: int = 94
    PART_TWO_EXPECTED_VALUE_TWO: int = 71
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(
        f"Part Two: {part_two(TEST_DATA_TWO)} (expected {PART_TWO_EXPECTED_VALUE_TWO})"
    )
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 8:51AM CST
