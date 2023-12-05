"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing
a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island
isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make
snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned
off the water a few days... weeks... oh no." His face sinks into a look of horrified
realization.

"I've been so busy making sure everyone here has food that I completely forgot to check
why we stopped getting more sand! There's a ferry leaving soon that is headed over in
that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you
wait for the ferry, maybe you can help us with our food production problem. The latest
Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also
lists what type of soil to use with each kind of seed, what type of fertilizer to use
with each kind of soil, what type of water to use with each kind of fertilizer, and so
on. Every type of seed, soil, fertilizer and so on is identified with a number, but
numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't
necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers
from a source category into numbers in a destination category. That is, the section
that starts with seed-to-soil map: describes how to convert a seed number (the source)
to a soil number (the destination). This lets the gardener and his team know which soil
to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by
one, the maps describe entire ranges of numbers that can be converted. Each line within
a map contains three numbers: the destination range start, the source range start,
and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a
range length of 2. This line means that the source range starts at 98 and contains two
values: 98 and 99. The destination range is the same length, but it starts at 50, so
its two values are 50 and 51. With this information, you know that seed number 98
corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values:
50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also
containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil
number 55.

Any source numbers that aren't mapped correspond to the same destination number. So,
seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like
this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to
know the closest location that needs a seed. Using these maps, find the lowest location
number that corresponds to any of the initial seeds. To do this, you'll need to convert
each seed number through other categories until you can find its corresponding location
number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the
almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value
is the start of the range and the second value is the length of the range. So, in the
first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first
range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The
second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27
seed numbers.

In the above example, the lowest location number can be obtained from seed number 82,
which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45,
humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the
almanac. What is the lowest location number that corresponds to any of the initial
seed numbers?

"""
from typing import List, NamedTuple
from pathlib import Path


class Range(NamedTuple):
    """A simple range data type."""

    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def __contains__(self, key: int) -> bool:
        return self.start <= key < self.start + self.length


class RangeMap:
    """One map that converts a range of numbers from one type to another."""

    def __init__(self, source_start: int, destination_start: int, length: int):
        self.source_range: Range = Range(source_start, length)
        self.destination_range: Range = Range(destination_start, length)

    @property
    def delta(self):
        return self.destination_range.start - self.source_range.start

    @property
    def input_range(self) -> Range:
        return self.source_range

    def __contains__(self, key: int) -> bool:
        return key in self.source_range

    def __getitem__(self, key: int) -> None:
        return key + self.delta


def propagate_range(range_: Range, range_maps: List[RangeMap]) -> List["Range"]:
    """Find the intersections of one range with a list of other (sorted) ranges."""
    ranges: List[Range] = []
    current_start = range_.start

    for r in range_maps:
        if r.source_range.end < range_.start:
            # The range is before the start of the original range
            continue

        if r.source_range.start > range_.end:
            # The range is beyond the end of the original range
            break

        if r.source_range.start > current_start:
            # Add segment before the current range starts, if any
            ranges.append(Range(current_start, r.source_range.start - current_start))

        # Add the intersecting segment
        intersect_start = max(current_start, r.source_range.start)
        intersect_end = min(range_.end, r.source_range.end)
        if intersect_end >= intersect_start:
            ranges.append(
                Range(intersect_start + r.delta, intersect_end - intersect_start + 1)
            )

        # Update the current start position for the next iteration
        current_start = intersect_end + 1

        if current_start > range_.end:
            break

    # Add the remaining segment, if any
    if current_start <= range_.end:
        ranges.append(Range(current_start, range_.end - current_start + 1))

    return ranges


class Almanac:
    """An almanac is used to convert a source range to a destination range."""

    def __init__(self, source: str, destination: str, data: List[str]):
        self.source = source
        self.destination = destination
        self.range_maps: List[RangeMap] = []
        self._parse_data(data)

    def _parse_data(self, data: List[str]):
        for line in data[1:]:
            destination_start, source_start, length = (
                int(value) for value in line.strip().split(" ")
            )
            self.range_maps.append(RangeMap(source_start, destination_start, length))

        self.range_maps = sorted(self.range_maps, key=lambda m: m.source_range.start)

    def __getitem__(self, key: int) -> int:
        for range_map in self.range_maps:
            if key in range_map:
                return range_map[key]
        return key


class RangeFarm:
    def __init__(self, data: List[str], part: int = 1):
        self.seeds: List[Range] = []
        self.maps: List[Almanac] = []
        self.part = part
        self._parse_data(data)

    def _parse_data(self, data: List[str]):
        # Split the data into a list of lists, separated by "" empty strings
        data_lists = []
        current_list = []
        for line in data:
            if line == "":
                data_lists.append(current_list)
                current_list = []
            else:
                current_list.append(line)
        data_lists.append(current_list)

        for data_list in data_lists:
            if data_list[0].startswith("seeds:"):
                self.seeds = self._parse_seeds(data_list[0])
            else:
                source_type, destination_type = data_list[0].strip().split("-to-")
                destination_type = destination_type.split(" ")[0]
                self.maps.append(Almanac(source_type, destination_type, data_list))

    def _parse_seeds(self, data_line: str) -> List[Range]:
        seeds: List[Range] = []
        value_list = [int(value) for value in data_line.split(":")[-1].strip().split()]
        if self.part == 1:
            # For part one, consider seed ranges of length 1
            for value in value_list:
                seeds.append(Range(value, 1))
            seeds = sorted(seeds, key=lambda r: r.start)
        else:
            for i in range(0, len(value_list), 2):
                seeds.append(Range(value_list[i], value_list[i + 1]))
            seeds = sorted(seeds, key=lambda r: r.start)
        return seeds

    @property
    def _locations(self) -> List[Range]:
        locations: List[Range] = []
        # For each seed range
        for seed in self.seeds:
            # Initialize the current type and range list
            current_type = "seed"
            current_ranges: List[Range] = [seed]
            # Keep propagating the ranges until we arrive at "location"
            while current_type != "location":
                # Cycle through the maps until we find the one that matches
                # the current type
                for almanac_map in self.maps:
                    if almanac_map.source == current_type:
                        # Split current set of ranges into new set of ranges
                        new_ranges: List[Range] = []
                        for _range in current_ranges:
                            new_ranges.extend(
                                propagate_range(_range, almanac_map.range_maps)
                            )
                        # Update the current type and ranges
                        current_type = almanac_map.destination
                        current_ranges = new_ranges
                        break
            # Add the minimum location for the current ranges to the list
            # since this is all we really care about
            locations.append(min([r.start for r in current_ranges]))
        return locations

    @property
    def lowest_location(self) -> int:
        return min(self._locations)


def part_one(data: List[str]) -> int:
    farm = RangeFarm(data, part=1)
    return farm.lowest_location


def part_two(data: List[str]) -> int:
    farm = RangeFarm(data, part=2)
    return farm.lowest_location


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(f"{WORKING_DIR}/data.csv", "r", encoding="utf-8").read().split("\n")
    TEST_DATA: List[str] = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]

    PART_ONE_EXPECTED_OUTPUT: int = 35
    # Starting Part One at 8:20AM CST
    print(
        f"Part One (Test): {part_one(TEST_DATA)} "
        f"(expected {PART_ONE_EXPECTED_OUTPUT})"
    )
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 9:12AM CST

    # Starting Part Two at 9:14AM CST
    PART_TWO_EXPECTED_OUTPUT: int = 46
    print(
        f"Part Two (Test): {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_OUTPUT})"
    )
    print(f"Part Two: {part_two(DATA)}")
    # Finished Part Two at 3:30PM CST
