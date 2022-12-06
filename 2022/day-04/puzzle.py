"""Day 4, 2022 Advent of Code puzzle solution

https://adventofcode.com/2022/day/4
"""

def main(data_file: str) -> None:
    with open(data_file) as f:
        lines = [line.strip() for line in f.readlines()]
    
    overlap = 0
    total_overlap = 0
    for line in lines:
        range1_str, range2_str = line.split(",")
        range1 = range_str_to_set(range1_str)
        range2 = range_str_to_set(range2_str)
        if range1.issubset(range2) or range2.issubset(range1):
            total_overlap += 1
            overlap += 1
        elif len(range1.intersection(range2)) > 0:
            overlap += 1
    
    print(f"Part 1 Solution: {total_overlap}")
    print(f"Part 2 Solution: {overlap}")


def range_str_to_set(range_str: str) -> list:
    """Convert a range string to a list of integers"""
    start, end = range_str.split("-")
    return set(range(int(start), int(end) + 1))

if __name__ == "__main__":
    main("puzzle_data.csv")