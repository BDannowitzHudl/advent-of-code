"""Day 3, 2022 Advent of Code puzzle solution

https://adventofcode.com/2022/day/3

"""
from itertools import islice

def main(data_file: str) -> None:
    
    with open(data_file) as f:
        lines = [line.strip() for line in f.readlines()]

    value = 0
    for line in lines:
        part1 = set(line[:len(line) // 2])
        part2 = set(line[len(line) // 2:])
        overlap = list(part1.intersection(part2))[0]
        value += map_char_to_value(overlap)

    print(f"Part 1 Solution: {value}")

    value = 0
    for elf1, elf2, elf3 in zip(*[iter(lines)] * 3):
        rucksack1 = set(elf1)
        rucksack2 = set(elf2)
        rucksack3 = set(elf3)
        badge = list(rucksack1.intersection(rucksack2, rucksack3))[0]
        value += map_char_to_value(badge)
    
    print(f"Part 2 Solution: {value}")


def map_char_to_value(char: str) -> int:
    """Map a-z to 1-26 and A-Z to 27-52"""
    if char.islower():
        return ord(char) - 96
    elif char.isupper():
        return ord(char) - 38
    else:
        raise ValueError(f"Unexpected character: {char}")
    
    
if __name__ == "__main__":
    main("puzzle_data.csv")