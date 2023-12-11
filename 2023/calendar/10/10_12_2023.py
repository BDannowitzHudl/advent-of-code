"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you
do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent
direction; maybe you can find someone at the hot springs and ask them where the
desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop
to admire some metal grass, you notice something metallic scurry away in your
peripheral vision and jump into a big pipe! It didn't look like any animal you've ever
seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely
packed with pipes; it was hard to tell at first because they're the same metallic
silver color as the "ground". You make a quick sketch of all of the surface pipes you
can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch
doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that
contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would
instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because
of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This
sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop:
they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that
is farthest from the starting position. Because the animal is in the pipe, it doesn't
make sense to measure this by direct distance. Instead, you need to find the tile that
would take the longest number of steps along the loop to reach from the starting point -
regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to
get from the starting position to the point farthest from the starting position?
"""
from typing import List
from pathlib import Path
from networkx import Graph, DiGraph
from shapely.geometry import Polygon, Point
import networkx as nx


def create_edge(graph: DiGraph, node_position: tuple, char: str) -> None:
    if char == ".":
        pass
    elif char == "|":
        if (node_position[0], node_position[1] - 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] - 1),
            )
        if (node_position[0], node_position[1] + 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] + 1),
            )
    elif char == "-":
        if (node_position[0] - 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] - 1, node_position[1]),
            )
        if (node_position[0] + 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] + 1, node_position[1]),
            )
    elif char == "L":
        if (node_position[0], node_position[1] - 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] - 1),
            )
        if (node_position[0] + 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] + 1, node_position[1]),
            )
    elif char == "J":
        if (node_position[0], node_position[1] - 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] - 1),
            )
        if (node_position[0] - 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] - 1, node_position[1]),
            )
    elif char == "7":
        if (node_position[0], node_position[1] + 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] + 1),
            )
        if (node_position[0] - 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] - 1, node_position[1]),
            )
    elif char == "F":
        if (node_position[0], node_position[1] + 1) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0], node_position[1] + 1),
            )
        if (node_position[0] + 1, node_position[1]) in graph.nodes:
            graph.add_edge(
                node_position,
                (node_position[0] + 1, node_position[1]),
            )
    elif char == "S":
        pass

    return None


def make_digraph(data: List[str]) -> DiGraph:
    height = len(data)
    width = len(data[0])
    graph = DiGraph()
    # Add a node for every position in the grid
    for y in range(height):
        for x in range(width):
            graph.add_node((x, y), char=data[y][x])
    # Now make the edges connect acording to the character of the node
    for node in graph.nodes(data=True):
        create_edge(graph, node[0], node[1]["char"])
    return graph


def digraph_to_graph(digraph: DiGraph) -> Graph:
    # Now create a new graph that is undirected, that only has an edge if
    # nodes are connected in both directions
    graph = Graph()
    for node in digraph.nodes(data=True):
        graph.add_node(node[0], char=node[1]["char"])
    for node in digraph.nodes(data=True):
        if node[1]["char"] == "S":
            # Look to see which edges connect TO the start node
            # Connect back to them
            for other_node in digraph.nodes:
                if digraph.has_edge(other_node, node[0]):
                    graph.add_edge(node[0], other_node)
    for node in digraph.nodes:
        for edge in digraph.edges(node):
            if digraph.has_edge(edge[1], edge[0]):
                graph.add_edge(edge[0], edge[1])
    return graph


def part_one(data: List[str]) -> int:
    dg = make_digraph(data)
    g = digraph_to_graph(dg)
    # Get the sub-graph that is connected to the start node
    # Get the starting node:
    for node in g.nodes(data=True):
        if node[1]["char"] == "S":
            start_node = node[0]
            break
    # This will be in a closed cyclical graph. Get just that sub-graph
    connected_nodes = nx.node_connected_component(g, start_node)
    return len(connected_nodes) // 2


def part_two(data: List[str]) -> int:
    dg = make_digraph(data)
    g = digraph_to_graph(dg)

    # Get the sub-graph that is connected to the start node
    # Get the starting node:
    for node in g.nodes(data=True):
        if node[1]["char"] == "S":
            start_node = node[0]
            break
    # This will be in a closed cyclical graph. Get just that sub-graph
    connected_nodes = nx.node_connected_component(g, start_node)
    sub_g = g.subgraph(connected_nodes)
    vertices: List[tuple] = [start_node]

    # Starting at the start node, follow the sub-graph throughone whole loop, saving
    # the vertices
    node = start_node
    while True:
        for edge in sub_g.edges(node):
            if edge[0] not in vertices:
                vertices.append(edge[0])
                node = edge[0]
                break
            elif edge[1] not in vertices:
                vertices.append(edge[1])
                node = edge[1]
                break
        else:
            break

    poly = Polygon(vertices)

    inside_count = 0
    inside_points = []
    for node in g.nodes:
        if node not in sub_g.nodes and poly.contains(Point(node)):
            inside_points.append(node)
            inside_count += 1

    import matplotlib.pyplot as plt

    # Plot and save the polygon
    _, ax = plt.subplots(figsize=(10, 10))
    x, y = poly.exterior.xy
    ax.plot(
        x,
        y,
        color="#6699cc",
    )
    ax.scatter(
        [x[0] for x in inside_points],
        [x[1] for x in inside_points],
        color="red",
        marker="x",
    )
    ax.set_title(f"Polygon with {len(inside_points)} points inside")
    WORKING_DIR = Path(__file__).parent
    plt.savefig(WORKING_DIR / "polygon.png")

    return inside_count


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA_ONE: List[str] = [
        "-L|F7",
        "7S-7|",
        "L|7||",
        "-L-J|",
        "L|-JF",
    ]
    TEST_DATA_TWO: List[str] = [
        "7-F7-",
        ".FJ|7",
        "SJLL7",
        "|F--J",
        "LJ.LJ",
    ]

    # Starting Part One at 8:17PM CST

    PART_ONE_EXPECTED_VALUE_ONE: int = 4
    PART_ONE_EXPECTED_VALUE_TWO: int = 8

    print(
        f"Part One: {part_one(TEST_DATA_ONE)} (expected {PART_ONE_EXPECTED_VALUE_ONE})"
    )
    print(
        f"Part One: {part_one(TEST_DATA_TWO)} (expected {PART_ONE_EXPECTED_VALUE_TWO})"
    )
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    TEST_DATA_THREE: List[str] = [
        "...........",
        ".S-------7.",
        ".|F-----7|.",
        ".||.....||.",
        ".||.....||.",
        ".|L-7.F-J|.",
        ".|..|.|..|.",
        ".L--J.L--J.",
        "...........",
    ]
    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE_THREE: int = 4
    print(
        f"Part Two: {part_two(TEST_DATA_THREE)} "
        f"(expected {PART_TWO_EXPECTED_VALUE_THREE})"
    )
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
