"""
--- Day 22: Sand Slabs ---
Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, piling up to form an
impressive stack here near the edge of Island Island. In order to make use of the sand
to filter water, some of the bricks will need to be broken apart - nay, disintegrated
- back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks
to disintegrate; if you disintegrate the wrong brick, large portions of the stack could
topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks
while they were still falling (your puzzle input) which should let you work out which
bricks are safe to disintegrate. For example:

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
Each line of text in the snapshot represents the position of a single brick at the time
the snapshot was taken. The position is given as two x,y,z coordinates - one for each
end of the brick - separated by a tilde (~). Each brick is made up of a single straight
line of cubes, and the Elves were even careful to choose a time for the snapshot that
had all of the free-falling bricks at integer positions above the ground, so the whole
snapshot is aligned to a three-dimensional cube grid.

A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate -
in other words, that the brick is a single cube.

Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in
volume, both oriented horizontally. The first brick extends in the x direction, while
the second brick extends in the y direction.

A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One
end of the brick is the cube located at 0,0,1, while the other end of the brick is
located directly above it at 0,0,10.

The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is
therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but
3,3,2~3,3,3 was above the ground at the time of the snapshot.

Because the snapshot was taken while the bricks were still falling, some bricks will
still be in the air; you'll need to start by figuring out where they will end up.
Bricks are magically stabilized, so they never rotate, even in weird situations like
where a long horizontal brick is only supported on one end. Two bricks cannot occupy
the same position, so a falling brick will come to rest upon the first other brick it
encounters.

Here is the same example again, this time with each brick given a letter so it can be
marked in diagrams:

1,0,1~1,2,1   <- A
0,0,2~2,0,2   <- B
0,2,3~2,2,3   <- C
0,0,4~0,2,4   <- D
2,0,5~2,2,5   <- E
0,1,6~2,1,6   <- F
1,1,8~1,1,9   <- G
At the time of the snapshot, from the side so the x axis goes left to right, these
bricks are arranged like this:

 x
012
.G. 9
.G. 8
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
Rotating the perspective 90 degrees so the y axis now goes left to right, the same
bricks are arranged like this:

 y
012
.G. 9
.G. 8
... 7
.F. 6
EEE 5 z
DDD 4
..C 3
B.. 2
AAA 1
--- 0
Once all of the bricks fall downward as far as they can go, the stack looks like this,
where ? means bricks are hidden behind other bricks at that location:

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0
Again from the side:

 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0
Now that all of the bricks have settled, it becomes easier to tell which bricks are
supporting which other bricks:

Brick A is the only brick supporting bricks B and C.
Brick B is one of two bricks supporting brick D and brick E.
Brick C is the other brick supporting brick D and brick E.
Brick D supports brick F.
Brick E also supports brick F.
Brick F supports brick G.
Brick G isn't supporting any bricks.
Your first task is to figure out which bricks are safe to disintegrate. A brick can be
safely disintegrated if, after removing it, no other bricks would fall further directly
downward. Don't actually disintegrate any bricks - just determine what would happen if,
for each brick, only that brick were disintegrated. Bricks can be disintegrated even if
they're completely surrounded by other bricks; you can squeeze between bricks if you
need to.

In this example, the bricks can be disintegrated as follows:

Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would
both fall.
Brick B can be disintegrated; the bricks above it (D and E) would still be supported by
brick C.
Brick C can be disintegrated; the bricks above it (D and E) would still be supported by
brick B.
Brick D can be disintegrated; the brick above it (F) would still be supported by brick
E.
Brick E can be disintegrated; the brick above it (F) would still be supported by brick
D.
Brick F cannot be disintegrated; the brick above it (G) would fall.
Brick G can be disintegrated; it does not support any other bricks.
So, in this example, 5 bricks can be safely disintegrated.

Figure how the blocks will settle based on the snapshot. Once they've settled, consider
disintegrating a single brick; how many bricks could be safely chosen as the one to get
disintegrated?

--- Part Two ---
Disintegrating bricks one at a time isn't going to be fast enough. While it might sound
dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. For each brick, determine how
many other bricks would fall if that brick were disintegrated.

Using the same example as above:

Disintegrating brick A would cause all 6 other bricks to fall.
Disintegrating brick F would cause only 1 other brick, G, to fall.
Disintegrating any other brick would cause no other bricks to fall. So, in this
example, the sum of the number of other bricks that would fall as a result of
disintegrating each brick is 7.

For each brick, determine how many other bricks would fall if that brick were
disintegrated. What is the sum of the number of other bricks that would fall?

"""
from typing import List, Optional
from pathlib import Path
import json
import networkx as nx


class Cube:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    @property
    def coords(self) -> List[int]:
        return [self.x, self.y, self.z]


class Brick:
    def __init__(self, name: int, start: str, end: str):
        self.name = name
        self.cubes = self.get_cubes(start, end)
        self.grounded = any([c.z == 1 for c in self.cubes])
        self.disintegrate_count: Optional[int] = None

    @property
    def start(self) -> str:
        return ",".join([str(c) for c in self.cubes[0].coords])

    @property
    def end(self) -> str:
        return ",".join([str(c) for c in self.cubes[-1].coords])

    def get_cubes(self, start: str, end: str) -> List[Cube]:
        start_x, start_y, start_z = start.split(",")
        end_x, end_y, end_z = end.split(",")
        return [
            Cube(x, y, z)
            for x in range(int(start_x), int(end_x) + 1)
            for y in range(int(start_y), int(end_y) + 1)
            for z in range(int(start_z), int(end_z) + 1)
        ]

    def supports(self, other: "Brick") -> bool:
        for self_cube in self.cubes:
            for other_cube in other.cubes:
                if (
                    self_cube.x == other_cube.x
                    and self_cube.y == other_cube.y
                    and self_cube.z == other_cube.z - 1
                ):
                    # If supported by a grounded brick, this brick is also grounded
                    if other.grounded:
                        self.grounded = True
                    return True
        return False

    @property
    def min_z(self) -> int:
        return min([c.z for c in self.cubes])

    @property
    def max_z(self) -> int:
        return max([c.z for c in self.cubes])

    def drop_v1(self):
        if not self.grounded:
            for cube in self.cubes:
                cube.z -= 1
            self.grounded = any([c.z == 1 for c in self.cubes])

    def drop(self, grounded_bricks: List["Brick"]):
        """Move from current z position to the next lowest z position, if possible.

        Place above the highest z position of any supporting bricks, or on the ground
        if no supporting bricks are found.
        """
        new_z = 1
        for falling_cube in self.cubes:
            for grounded_brick in grounded_bricks:
                for grounded_cube in grounded_brick.cubes:
                    if (
                        falling_cube.x == grounded_cube.x
                        and falling_cube.y == grounded_cube.y
                    ):
                        new_z = max(new_z, grounded_cube.z + 1)
        dz = self.min_z - new_z
        for cube in self.cubes:
            cube.z -= dz
        self.grounded = True

    def __repr__(self):
        return f"{self.start}~{self.end}"

    def __str__(self):
        return self.__repr__()


class BrickStack:
    def __init__(self, bricks: List[Brick]):
        self.bricks = bricks

    def settle_v1(self):
        changes = 1
        while changes > 0:
            changes = 0
            for b1 in self.bricks:
                if b1.grounded:
                    continue
                supported = False
                for b2 in [b for b in self.bricks if b.max_z < b1.min_z]:
                    if b2.supports(b1):
                        supported = True
                        break
                if not b1.grounded and not supported:
                    b1.drop()
                    changes += 1

    def settle(self):
        grounded_bricks = [b for b in self.bricks if b.grounded]
        non_grounded_bricks = [b for b in self.bricks if not b.grounded]
        non_grounded_bricks.sort(key=lambda b: b.min_z)
        counter = 0
        for bottom_brick in non_grounded_bricks:
            bottom_brick.drop(grounded_bricks)
            grounded_bricks.append(bottom_brick)
            counter += 1

    def support_dict(self) -> dict:
        # Go through each brick, and find the bricks that can support it
        support_dict = {}
        # Should be {brick: [supporting_bricks]}
        for brick in self.bricks:
            support_dict[brick.name] = []
            beneath_bricks = [b for b in self.bricks if b.max_z == brick.min_z - 1]
            for beneath_brick in beneath_bricks:
                if beneath_brick.supports(brick):
                    support_dict[brick.name].append(beneath_brick.name)

        with open("support_dict.json", "w", encoding="utf-8") as f:
            json.dump(support_dict, f, indent=4)
        return support_dict

    def disintegratable(self) -> List[str]:
        support_dict = self.support_dict()
        disintegratable = [str(b.name) for b in self.bricks]
        for _, supports in support_dict.items():
            if len(supports) == 1:
                if str(supports[0]) in disintegratable:
                    disintegratable.remove(str(supports[0]))
        return disintegratable

    def __repr__(self):
        return "\n".join([str(b) for b in self.bricks])


def part_one(data: List[str]) -> int:
    bricks = []
    for i, line in enumerate(data):
        start, end = line.split("~")
        bricks.append(Brick(i, start, end))
    brick_stack = BrickStack(bricks)
    print("Settling...")
    brick_stack.settle()
    print("Counting...")
    disintegratable = brick_stack.disintegratable()
    return len(disintegratable)


def avalanche(dg: nx.DiGraph) -> int:
    count = 0
    if dg.nodes == ["ground"]:
        return 0
    dg_copy = dg.copy()
    for node in dg.nodes:
        if node == "ground":
            continue
        if len(dg.in_edges(node)) == 0:
            dg_copy.remove_node(node)
            count += 1
    if any(
        [len(dg_copy.in_edges(node)) == 0 for node in dg_copy.nodes if node != "ground"]
    ):
        count += avalanche(dg_copy)
    return count


def part_two(data: List[str]) -> int:
    bricks = []
    for i, line in enumerate(data):
        start, end = line.split("~")
        bricks.append(Brick(i, start, end))
    brick_stack = BrickStack(bricks)
    print("Settling...")
    brick_stack.settle()

    dg = nx.DiGraph()
    support_dict = brick_stack.support_dict()
    for brick, supports in support_dict.items():
        for support in supports:
            dg.add_edge(str(support), str(brick))
        if supports == []:
            dg.add_edge("ground", str(brick))

    disintegratable = brick_stack.disintegratable()
    bricks = [
        str(b.name) for b in brick_stack.bricks if str(b.name) not in disintegratable
    ]
    count = 0
    print("Counting...")
    for node in dg.nodes:
        if node == "ground":
            continue
        dg_copy = dg.copy()
        dg_copy.remove_node(node)
        count += avalanche(dg_copy)
    return count


def part_two_test():
    dg = nx.DiGraph()
    dg.add_edge("ground", "L")
    dg.add_edge("L", "A")
    dg.add_edge("L", "B")
    dg.add_edge("A", "C")
    dg.add_edge("A", "M")
    dg.add_edge("B", "C")
    dg.add_edge("C", "D")
    dg.add_edge("C", "E")
    dg.add_edge("E", "F")
    dg.add_edge("E", "G")
    dg.add_edge("D", "F")
    dg.add_edge("M", "H")
    dg.add_edge("F", "H")
    dg.add_edge("F", "I")
    dg.add_edge("F", "J")
    dg.add_edge("I", "K")
    dg.add_edge("H", "K")
    dg.add_edge("J", "K")
    count = 0
    for node in dg.nodes:
        if node == "ground":
            continue
        dg_copy = dg.copy()
        dg_copy.remove_node(node)
        count += avalanche(dg_copy)

    print(count, "should be 22")


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "1,0,1~1,2,1",
        "0,0,2~2,0,2",
        "0,2,3~2,2,3",
        "0,0,4~0,2,4",
        "2,0,5~2,2,5",
        "0,1,6~2,1,6",
        "1,1,8~1,1,9",
    ]

    # Starting Part One at 7:50AM CST

    PART_ONE_EXPECTED_VALUE: int = 5
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 7
    # part_two_test()
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 3:55PM CST
