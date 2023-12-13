"""
--- Day 12: Hot Springs ---
You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.

As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

You look in the direction the researcher is pointing and suddenly notice the massive
metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive fenced-off
area containing the springs. You go through the gate and into a small administrative
building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot right now;
we're having a lava shortage at the moment." You ask about the missing machine parts
for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the
moment, not until we get more lava to heat our forges. And our springs. The springs
aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? The springs are too cold
for normal operation, but we should be able to find one springy enough to launch you
up there!"

There's just one problem - many of the springs have fallen into disrepair, so they're
not actually sure which springs would even be safe to use! Worse yet, their condition
records of which springs are damaged (your puzzle input) are also damaged! You'll need
to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the
condition records show every spring and whether it is operational (.) or damaged (#).
This is the part of the condition records that is itself damaged; for some springs, it
is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this
information in a different format! After the list of springs for a given row, the size
of each contiguous group of damaged springs is listed in the order those groups appear
in the row. This list always accounts for every damaged spring, and each number is the
entire size of its contiguous group (that is, groups are always separated by at least
one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
However, the condition records are partially damaged; some of the springs' conditions
are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
Equipped with this information, it is your job to figure out how many different
arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one,
one, and three broken springs (in that order) can appear in that row: the first three
unknown springs must be broken, then operational, then broken (#.#), making the whole
row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four
different arrangements. The last ? must always be broken (to satisfy the final
contiguous group of three broken springs), and each ?? must hide exactly one of the
two broken springs. (Neither ?? could be both broken springs or they would form a
single contiguous group of two; if that were true, the numbers afterward would have
been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible
arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the
first number is 3, the first and second ? must both be . (if either were #, the first
number would have to be 4 or higher). However, the remaining run of unknown spring
conditions have many different ways they could hold groups of two and one broken
springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
In this example, the number of possible arrangements for each row is:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 4 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 1 arrangement
????.######..#####. 1,6,5 - 4 arrangements
?###???????? 3,2,1 - 10 arrangements
Adding all of the possible arrangement counts together produces a total of 21
arrangements.

For each row, count all of the different arrangements of operational and broken springs
that meet the given criteria. What is the sum of those counts?

--- Part Two ---
As you look out at the field of springs, you feel like there are way more springs than
the condition records list. When you examine the records, you discover that they were
actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with five
copies of itself (separated by ?) and replace the list of contiguous groups of damaged
springs with five copies of itself (separated by ,).

So, this row:

.# 1
Would become:

.#?.#?.#?.#?.# 1,1,1,1,1
The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
In the above example, after unfolding, the number of possible arrangements for some
rows is now much larger:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements
After unfolding, adding all of the possible arrangement counts together produces 525152.

Unfold your condition records; what is the new sum of possible arrangement counts?

"""
from typing import List
from pathlib import Path
from enum import Enum
from tqdm import tqdm


class Spring(Enum):
    WORKING = "."
    BROKEN = "#"
    UNKNOWN = "?"


class Validity(Enum):
    VALID = 1
    INVALID = 0
    UNKNOWN = -1


class SpringRecord:
    def __init__(self, line: str, part: int = 1):
        self.part = part
        self.line = line
        self.springs: List[Spring] = []
        self.groups: List[int] = []
        self._parse_line(line)
        self.valid: Validity = self._validate()

    def _parse_line(self, line: str):
        springs, groups = line.split(" ")
        self.springs = [Spring(s) for s in list(springs)]
        self.groups = [int(group) for group in groups.split(",")]

    def _validate(self) -> Validity:
        groups: List[int] = []
        group_size: int = 0
        for spring in self.springs:
            if spring == Spring.BROKEN:
                group_size += 1
            elif Spring.UNKNOWN in self.springs:
                return Validity.UNKNOWN
            else:
                if group_size > 0:
                    if (
                        len(groups) >= len(self.groups)
                        or group_size != self.groups[len(groups)]
                    ):
                        return Validity.INVALID
                    else:
                        groups.append(group_size)
                        group_size = 0
        if group_size > 0:
            groups.append(group_size)
        if groups == self.groups:
            return Validity.VALID

    def __str__(self) -> str:
        return (
            "".join([s.value for s in self.springs])
            + " "
            + ",".join(str(g) for g in self.groups)
        )

    def copy(self) -> "SpringRecord":
        return SpringRecord(str(self))

    @property
    def combinations(self) -> int:
        if self.valid == Validity.VALID:
            # If there's no unknown springs and the groups match,
            # there's only one combination
            return 1
        if Spring.UNKNOWN not in self.springs:
            return 0
        # Try replacing the first unknown spring with a working and broken spring
        first_unknown = self.springs.index(Spring.UNKNOWN)

        working_list = list(self.line)
        working_list[first_unknown] = Spring.WORKING.value
        working_str = "".join(working_list)
        working = SpringRecord(working_str)

        broken_list = list(self.line)
        broken_list[first_unknown] = Spring.BROKEN.value
        broken_str = "".join(broken_list)
        broken = SpringRecord(broken_str)

        combinations: int = 0
        if working.valid != Validity.INVALID:
            combinations += working.combinations
        if broken.valid != Validity.INVALID:
            combinations += broken.combinations

        return combinations


def part_one(data: List[str]) -> int:
    spring_records: List[SpringRecord] = [SpringRecord(line) for line in data]
    total: int = 0
    for sr in tqdm(spring_records, ncols=80):
        total += sr.combinations
    return total


def part_two(data: List[str]) -> int:
    spring_records: List[SpringRecord] = [SpringRecord(line, part=2) for line in data]
    total: int = 0
    for sr in tqdm(spring_records, ncols=80):
        print(str(sr), sr.combinations)
        combinations = sr.combinations**5
        if sr.springs[-1] == Spring.BROKEN:
            combinations *= 2**4
        total += combinations
    return total


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]

    # Starting Part One at 10:20AM CST

    PART_ONE_EXPECTED_VALUE: int = 21
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    # print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 11:15AM CST

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 525152
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    # print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at
