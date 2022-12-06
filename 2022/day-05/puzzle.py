"""Day 5, 2022 Advent of Code puzzle solution

https://adventofcode.com/2022/day/5

"""
from copy import deepcopy


def main(data_csv: str, arrangement_csv: str):
    with open(data_csv) as f:
        lines = [line.strip() for line in f.readlines()]
    
    with open(arrangement_csv, 'r') as reader:
        text = reader.read()
        
    # Transpose the text file so the stacks are at least in line
    stack_str_list = [
        ''.join(chars).strip(" []")[::-1]
        for chars in zip(*text.splitlines())
    ]
    stack_str_list = [s for s in stack_str_list if s != '']
    part1_stacks = {int(s[0]): list(s[1:]) for s in stack_str_list}
    part2_stacks = deepcopy(part1_stacks)

    # Move the boxes
    for line in lines:
        instructions = line.split(" ")
        n_boxes = int(instructions[1])
        source = int(instructions[3])
        destination = int(instructions[5])
        part1_stacks = move_boxes(part1_stacks, n_boxes, source, destination)
        part2_stacks = crate_mover_9001(part2_stacks, n_boxes, source, destination)

    print("Part 1: ", end="")
    for i in range(1, len(part1_stacks) + 1):
        print(part1_stacks[i][-1], end="")

    print()
    print("Part 2: ", end="")
    for i in range(1, len(part2_stacks) + 1):
        print(part2_stacks[i][-1], end="")
    print()


def move_boxes(stacks: dict[int, list[int]], n_boxes: int, source: int, destination: int):
    """Move n_boxes from source to destination"""
    # Move the boxes from the source to the destination
    for _ in range(n_boxes):
        stacks[destination].append(stacks[source].pop())
    return stacks

def crate_mover_9001(stacks: dict[int, list[int]], n_boxes: int, source: int, destination: int):
    for box in stacks[source][-n_boxes:]:
        stacks[destination].append(box)
    # Remove the boxes from the source
    stacks[source] = stacks[source][:-n_boxes]
    return stacks

if __name__ == "__main__":
    main("puzzle_data.csv", "arrangement.dat")
    