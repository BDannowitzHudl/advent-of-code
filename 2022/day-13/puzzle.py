"""Day 13, 2022 Advent of Code puzzle solution.

https://adventofcode.com/2022/day/13
"""
from typing import List, Union
import ast
from enum import Enum, auto


class Instruction(Enum):
    RIGHT_ORDER = auto()
    WRONG_ORDER = auto()
    CONTINUE = auto()

    
def right_order(
    left: Union[int, List[int]],
    right: Union[int, List[int]]
) -> Instruction:

    # Both are ints
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return Instruction.RIGHT_ORDER
        elif left > right:
            return Instruction.WRONG_ORDER
        else:
            return Instruction.CONTINUE

    # Mixed types
    elif isinstance(left, int) and isinstance(right, list):
        return right_order([left,], right)
    elif isinstance(left, list) and isinstance(right, int):
        return right_order(left, [right,])

    # Both are lists
    else:
        left_len, right_len = len(left), len(right)
        for i in range(left_len):
            # If the right runs out of elements, wrong order
            if i + 1 > right_len:
                return Instruction.WRONG_ORDER
            order_eval = right_order(left[i], right[i])
            if order_eval == Instruction.CONTINUE:
                continue
            else:
                return order_eval
        if left_len < right_len:
            return Instruction.RIGHT_ORDER    
        else:
            return Instruction.CONTINUE
        

def quicksort(array):
    if len(array) > 1:
        pivot = array[-1]
        higher = []
        lower = []
        for element in array[:-1]:
            if right_order(element, pivot) == Instruction.RIGHT_ORDER:
                lower.append(element)
            else:
                higher.append(element)
        return quicksort(lower) + [pivot,] + quicksort(higher)
    else:
        return array


def main(data_file: str):

    with open(data_file, 'r') as f:
        data = f.read().splitlines()
    
    score = 0    
    for i in range(len(data) // 3 + 1):
        left = ast.literal_eval(data[i*3])
        right = ast.literal_eval(data[i*3 + 1])
        if right_order(left, right) == Instruction.RIGHT_ORDER:
            score += i+1

    print(f"Part 1: {score}")
    
    packets = []
    for line in data:
        if line != "":
            packets.append(ast.literal_eval(line))
    packets.append([[6,]])
    packets.append([[2,]])
    
    # Quicksort time!
    sorted_packets = quicksort(packets)
    score = (
        (sorted_packets.index([[6,]]) + 1) *
        (sorted_packets.index([[2,]]) + 1)
    )
    print(f"Part 2: {score}")


if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
