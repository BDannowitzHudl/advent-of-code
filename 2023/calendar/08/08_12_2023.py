"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly
approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair,
she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents
(your puzzle input) about how to navigate the desert. At least, you're pretty sure
that's what they are; one of the documents contains a list of left/right instructions,
and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network.
Perhaps if you have the camel follow the same instructions, you can escape the haunted
wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA
is where you are now, and you have to follow the left/right instructions until you
reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right
instruction in your input. In this example, start with AAA and go right (R) by choosing
the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By
following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions,
repeat the whole sequence of instructions as necessary: RL really means
RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to
reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to
reach ZZZ?

--- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had
the camel follow the instructions, but you've barely left your starting position. It's
going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound
by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the
number of nodes with names ending in A is equal to the number ending in Z! If you were
a ghost, you'd probably just start at every node that ends with A and follow all of
the paths at the same time until they all simultaneously end up at nodes that end
with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
Here, there are two starting nodes, 11A and 22A (because they both end with A). As you
follow each left/right instruction, use that instruction to simultaneously navigate
away from both nodes you're currently on. Repeat this process until all of the nodes
you're currently on end with Z. (If only some of the nodes you're on end with Z, they
act like any other node and you continue as normal.) In this example, you would proceed
as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before
you're only on nodes that end with Z?

"""
from typing import List
from pathlib import Path
from networkx import DiGraph
from itertools import cycle
from functools import reduce


def make_graph(data: List[str]) -> DiGraph:
    g = DiGraph()
    for line in data[2:]:
        source_node, connected_nodes = line.split(" = ")
        left_node, right_node = (
            connected_nodes.replace("(", "").replace(")", "").split(", ")
        )
        g.add_edge(source_node, left_node, L=True)
        g.add_edge(source_node, right_node, R=True)
    return g


def part_one(data: List[str]) -> int:
    directions = data[0]
    start_node = "AAA"
    destination_node = "ZZZ"
    g = make_graph(data)

    steps: int = 0
    node = start_node
    for d in cycle(directions):
        if node == destination_node:
            return steps
        node = next(v for _, v, attr in g.edges(node, data=True) if attr.get(d))
        steps += 1
    return -1


def lcm(numbers: List[int]) -> int:
    """Return lowest common multiple."""

    def lcm_two(a: int, b: int) -> int:
        """Return lowest common multiple of two numbers."""
        return (a * b) // gcd(a, b)

    def gcd(a: int, b: int) -> int:
        """Return greatest common divisor of two numbers."""
        while b:
            a, b = b, a % b
        return a

    return reduce(lcm_two, numbers, 1)


def part_two(data: List[str]) -> int:
    directions = data[0]
    g = make_graph(data)

    current_nodes = [n for n in g.nodes if n.endswith("A")]
    n_steps: List[int] = [0] * len(current_nodes)
    steps_to_z: List[int] = [0] * len(current_nodes)
    for d in cycle(directions):
        if all(n.endswith("Z") for n in current_nodes):
            return steps
        for idx, node in enumerate(current_nodes):
            current_nodes[idx] = next(
                v for _, v, attr in g.edges(node, data=True) if attr.get(d)
            )
            n_steps[idx] += 1
            if current_nodes[idx].endswith("Z"):
                steps_to_z[idx] = n_steps[idx]
        if all(steps_to_z):
            steps = lcm(steps_to_z)
            return steps
    return -1


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA_ONE: List[str] = [
        "RL",
        "",
        "AAA = (BBB, CCC)",
        "BBB = (DDD, EEE)",
        "CCC = (ZZZ, GGG)",
        "DDD = (DDD, DDD)",
        "EEE = (EEE, EEE)",
        "GGG = (GGG, GGG)",
        "ZZZ = (ZZZ, ZZZ)",
    ]
    TEST_DATA_TWO: List[str] = [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)",
    ]

    # Starting Part One at 8:46 AM CST

    PART_ONE_EXPECTED_VALUE_ONE: int = 2
    PART_ONE_EXPECTED_VALUE_TWO: int = 6
    print(
        f"Part One: {part_one(TEST_DATA_ONE)} (expected {PART_ONE_EXPECTED_VALUE_ONE})"
    )
    print(
        f"Part One: {part_one(TEST_DATA_TWO)} (expected {PART_ONE_EXPECTED_VALUE_TWO})"
    )
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 9:05 AM CST

    # Starting Part Two at 9:09 AM CST

    PART_TWO_TEST_DATA: List[str] = [
        "LR",
        "",
        "11A = (11B, XXX)",
        "11B = (XXX, 11Z)",
        "11Z = (11B, XXX)",
        "22A = (22B, XXX)",
        "22B = (22C, 22C)",
        "22C = (22Z, 22Z)",
        "22Z = (22B, 22B)",
        "XXX = (XXX, XXX)",
    ]
    PART_TWO_EXPECTED_VALUE: int = 6
    print(
        f"Part Two: {part_two(PART_TWO_TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})"
    )
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 9:23 AM CST
