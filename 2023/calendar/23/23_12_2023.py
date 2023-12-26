"""
--- Day 23: A Long Walk ---
The Elves resume water filtering operations! Clean water starts flowing over the edge
of Island Island.

They offer to help you go over the edge of Island Island, too! Just hold on tight to
one end of this impossibly long rope and they'll lower you down a safe distance from
the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the
ground: it's being absorbed by the air itself. It looks like you'll finally have a
little downtime while the moisture builds up to snow-producing levels. Snow Island
is pretty scenic, even without any snow; why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates paths (.),
forest (#), and steep slopes (^, >, v, and <).

For example:

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
You're currently on the single path tile in the top row; your goal is to reach the
single path tile in the bottom row. Because of all the mist from the waterfall, the
slopes are probably quite icy; if you step onto a slope tile, your next step must be
downhill (in the direction the arrow is pointing). To make sure you have the most
scenic hike possible, never step onto the same tile twice. What is the longest hike
you can take?

In the example above, the longest hike you can take is marked with O, and your
starting position is marked S:

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
This hike contains 94 steps. (The other possible hikes you could have taken were 90,
86, 82, 82, and 74 steps long.)

Find the longest hike you can take through the hiking trails listed on your map. How
many steps long is the longest hike?

--- Part Two ---
As you reach the trailhead, you realize that the ground isn't as slippery as you
expected; you'll have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). You still want to make sure
you have the most scenic hike possible, so continue to ensure that you never step onto
the same tile twice. What is the longest hike you can take?

In the example above, this increases the longest hike to 154 steps:

#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
Find the longest hike you can take through the surprisingly dry hiking trails listed
on your map. How many steps long is the longest hike?
"""
from typing import List, Tuple
from pathlib import Path
from uuid import uuid4
from itertools import combinations
from tqdm import tqdm
import networkx as nx


def make_graph(data: List[str], part: int = 1) -> nx.DiGraph:
    if part == 1:
        dg = nx.DiGraph()
    else:
        dg = nx.Graph()
    n = len(data)
    m = len(data[0])
    for y in range(n):
        for x in range(m):
            if data[y][x] == "#":
                continue
            elif data[y][x] == "." or (part == 2 and data[y][x] in "^>v<"):
                # Check the four directions
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if 0 <= x + dx < m and 0 <= y + dy < n:
                        if data[y + dy][x + dx] != "#":
                            dg.add_edge((x, y), (x + dx, y + dy), weight=1)
            elif data[y][x] == "^":
                # Only check the up direction
                if 0 <= y - 1 < n:
                    if data[y - 1][x] != "#":
                        dg.add_edge((x, y), (x, y - 1), weight=1)
            elif data[y][x] == ">":
                # Only check the right direction
                if 0 <= x + 1 < m:
                    if data[y][x + 1] != "#":
                        dg.add_edge((x, y), (x + 1, y), weight=1)
            elif data[y][x] == "v":
                # Only check the down direction
                if 0 <= y + 1 < n:
                    if data[y + 1][x] != "#":
                        dg.add_edge((x, y), (x, y + 1), weight=1)
            elif data[y][x] == "<":
                # Only check the left direction
                if 0 <= x - 1 < m:
                    if data[y][x - 1] != "#":
                        dg.add_edge((x, y), (x - 1, y), weight=1)

    return dg


def longest_path_dfs(graph, start, end, path=[], longest=[0, []]):
    path = path + [start]
    if start == end:
        if len(path) > longest[0]:
            longest[0] = len(path)
            longest[1] = path
    for node in graph.neighbors(start):
        if node not in path:
            longest_path_dfs(graph, node, end, path, longest)
    return longest[1]


def longest_path_iterative(graph, start, end):
    longest_path = []
    stack = [(start, [start])]

    while stack:
        (vertex, path) = stack.pop()
        for next_step in set(graph.neighbors(vertex)) - set(path):
            if next_step == end:
                if len(path + [next_step]) > len(longest_path):
                    longest_path = path + [next_step]
            else:
                stack.append((next_step, path + [next_step]))

    return longest_path


def longest_path_iterative_by_weight(graph, start, end):
    longest_path = []
    longest_path_weight = 0
    stack = [(start, [start], 0)]  # Include path weight in the stack

    while stack:
        (vertex, path, path_weight) = stack.pop()
        for next_step in set(graph.neighbors(vertex)) - set(path):
            # Calculate the weight of the new edge
            new_edge_weight = graph[vertex][next_step]["weight"]
            new_path_weight = path_weight + new_edge_weight

            if next_step == end:
                # Compare total weights instead of path lengths
                if new_path_weight > longest_path_weight:
                    longest_path = path + [next_step]
                    longest_path_weight = new_path_weight
            else:
                stack.append((next_step, path + [next_step], new_path_weight))

    return longest_path


def simplify_graph(G: nx.Graph, start_node: Tuple[int, int], end_node: Tuple[int, int]):
    """Simplifies the graph by removing intermediate nodes and updating edge weights."""
    simplified_G = nx.Graph()
    connector_nodes = [n for n in G.nodes() if G.degree(n) > 2]

    combos = list(combinations(connector_nodes, 2))
    for cn1, cn2 in tqdm(combos, total=len(combos)):
        # Find paths to other connector nodes
        if cn1 == cn2:
            continue
        G_copy = G.copy()
        for node in connector_nodes:
            if node not in [cn1, cn2]:
                G_copy.remove_node(node)
        # Find all paths from cn to other_cn
        for path in nx.all_simple_paths(G_copy, cn1, cn2):
            # if the path doesn't contain another connector node
            if len(path) == 2:
                # If the path is just two nodes, connect them
                simplified_G.add_edge(cn1, cn2, weight=1)
            else:
                new_node = str(uuid4())
                simplified_G.add_edge(cn1, new_node, weight=0)
                simplified_G.add_edge(new_node, cn2, weight=len(path) - 1)

    # Finally, connect the start and end nodes to the connector nodes
    for terminal_node in [start_node, end_node]:
        for cn in connector_nodes:
            #  Find all simple paths from node to cn
            G_copy = G.copy()
            for node in connector_nodes:
                if node not in [start_node, end_node, cn]:
                    G_copy.remove_node(node)
            for path in nx.all_simple_paths(G_copy, terminal_node, cn):
                if cn in G.neighbors(node):
                    simplified_G.add_edge(terminal_node, cn, weight=1)
                    continue
                else:
                    new_node = str(uuid4())
                    simplified_G.add_edge(terminal_node, new_node, weight=0)
                    simplified_G.add_edge(new_node, cn, weight=len(path) - 1)

    return simplified_G


def longest_path_iterative_memoized(graph, start, end):
    if start == end:
        return [start]

    longest_paths = {node: None for node in graph.nodes()}
    longest_paths[end] = [end]
    stack = [start]

    while stack:
        node = stack[-1]

        if longest_paths[node] is not None:
            stack.pop()
            continue

        paths = []
        for neighbor in graph.neighbors(node):
            if longest_paths[neighbor] is not None:
                paths.append([node] + longest_paths[neighbor])

        if paths:
            longest_paths[node] = max(paths, key=len)
            stack.pop()
        else:
            stack.extend(set(graph.neighbors(node)) - set(stack))

    return longest_paths[start]


def part_one(data: List[str]) -> int:
    dg = make_graph(data)
    start = (1, 0)
    end = (len(data[0]) - 2, len(data) - 1)
    longest_path = longest_path_iterative(dg, start, end)
    return len(longest_path) - 1


def part_two(data: List[str]) -> int:
    g = make_graph(data, part=2)
    start = (1, 0)
    end = (len(data[0]) - 2, len(data) - 1)
    print(f"number of edges: {g.number_of_edges()}")
    g2 = simplify_graph(g, start, end)
    print(f"number of edges: {g2.number_of_edges()}")
    longest_path = longest_path_iterative_by_weight(g2, start, end)
    score = sum(
        g2.get_edge_data(u, v)["weight"] for u, v in zip(longest_path, longest_path[1:])
    )
    return score


def create_y_shaped_graph():
    """Create a Y-shaped graph."""
    G = nx.Graph()

    # Main branch (A -> B -> C -> D)
    G.add_edge("A", "B", weight=1)
    G.add_edge("B", "C", weight=1)

    # First branch from C (C -> E -> F)
    G.add_edge("C", "E", weight=1)
    G.add_edge("E", "F", weight=1)

    # Second branch from C (C -> G -> H)
    G.add_edge("C", "G", weight=1)
    G.add_edge("G", "H", weight=1)

    G.add_edge("F", "G", weight=1)

    return G


def tester():
    import matplotlib.pyplot as plt

    g = create_y_shaped_graph()
    print(g.edges(data=True))
    nx.draw(g, with_labels=True)
    # Save to file
    plt.savefig("graph.png")
    plt.close()

    g = simplify_graph(g, "A", "H")
    print(g.edges(data=True))
    nx.draw(g, with_labels=True)
    plt.savefig("simplified_graph.png")
    plt.close()


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()
    TEST_DATA = (
        open(WORKING_DIR / "test_data.csv", encoding="utf-8").read().splitlines()
    )

    # Starting Part One at 7:00 AM CST

    PART_ONE_EXPECTED_VALUE: int = 94
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    # print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at

    # tester()

    PART_TWO_EXPECTED_VALUE: int = 154
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
