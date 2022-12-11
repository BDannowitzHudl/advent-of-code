"""Day 11, 2022 Advent of Code puzzle solution.

Problem: Monkey Business
https://adventofcode.com/2022/day/11
"""
from typing import List, Dict, Optional
import re
from math import floor
from tqdm import tqdm
import numpy as np


class Monkey:
    
    def __init__(
        self,
        id: int,
        items: List[int],
        operation: str,
        test_div: int,
        true_target: int,
        false_target: int,
        worry_mitigation: int,
    ):
        self.id = id
        self.items = items
        self.inspect_op = operation.split(" ")[0]
        self.inspect_val = operation.split(" ")[1] 
        self.test_div = test_div
        self.target: Dict[bool, int] = {
            True: true_target,
            False: false_target,
        }
        self.inspect_count = 0
        self.worry_mitigation = worry_mitigation

    def inspect(self, modulo: Optional[int]):
        operand = self.items[0] if self.inspect_val == "old" else int(self.inspect_val)
        self.items[0] = int(eval(f"{self.items[0]} {self.inspect_op} {operand}"))

        if modulo is not None:
            self.items[0] = self.items[0] % modulo

        self.items[0] = floor(self.items[0] / self.worry_mitigation)

        self.inspect_count += 1

    def test(self):
        try:
            return self.items[0] % self.test_div == 0
        except Exception as e:
            print(self.items[0], self.test_div)

    def __repr__(self):
        print(f"Monkey {self.id} has {self.items}")


def create_monkey_list(data_file: str, worry_mitigation: int):

    with open(data_file, 'r') as f:
        data = f.read().splitlines()

    monkey_list: List[Monkey] = []
    for m in range((len(data) // 7) + 1):
        # If the line starts with "Monkey N:", capture the N of the monkey
        monkey_number = int(
            re.match(
                r'^Monkey (\d+):$',
                data[7 * m]
            ).group(1)
        )

        # Next line starts with "Starting items: A, B, C, D, E, F
        # Capture the items
        items = list(int(x) for x in
            re.match(
                r'  Starting items: (.*)$',
                data[7 * m + 1]
            ).group(1).split(", ")
        )

        # Next line starts with "Operation: new = A op B"
        operation  = re.match(
            r'  Operation: new = old (. [a-z0-9]+)$',
            data[(7 * m) + 2]
        ).group(1)

        # Next line starts with "Test: divisible by N
        # Capture the value of N
        divisible  = int(re.match(
            r'  Test: divisible by ([0-9]+)$',
            data[(7 * m) + 3]
        ).group(1))
        
        # Next line starts with "If true: throw to monkey N"
        true_target = int(re.match(
            r'    If true: throw to monkey ([0-9]+)$',
            data[(7 * m) + 4]
        ).group(1))
        false_target = int(re.match(
            r'    If false: throw to monkey ([0-9]+)$',
            data[(7 * m) + 5]
        ).group(1))
        monkey_list.append(
            Monkey(
                id=monkey_number,
                items=items,
                operation=operation,
                test_div=divisible,
                true_target=true_target,
                false_target=false_target,
                worry_mitigation=worry_mitigation,
            )
        )
    return monkey_list


def process_round(monkey_list: List[Monkey]):
    modulo = np.product(list(m.test_div for m in monkey_list))
    for monkey in monkey_list:
        for _ in range(len(monkey.items)):
            # Perform the operation and divide by 3
            monkey.inspect(modulo=modulo)
            # See what the test result is
            test_result = monkey.test()
            # Pop this item and pass it to the monkey based on the test result
            monkey_list[
                monkey.target[test_result]
            ].items.append(monkey.items.pop(0))
    

def main(data_file: str):

    monkey_list = create_monkey_list(data_file, worry_mitigation = int(3))
    rounds = 20
    for _ in tqdm(range(rounds), desc="Processing rounds", total=rounds):
        process_round(monkey_list)
                
    inspect_counts = sorted([m.inspect_count for m in monkey_list])
    score = inspect_counts[-2] * inspect_counts[-1]
    print(f"Part 1: {score}")
    
    monkey_list = create_monkey_list(data_file, worry_mitigation = int(1))
    rounds = 10_000
    for _ in tqdm(range(rounds), desc="Processing rounds", total=rounds):
        process_round(monkey_list)
                
    inspect_counts = sorted([m.inspect_count for m in monkey_list])
    score = inspect_counts[-2] * inspect_counts[-1]
    print(f"Part 2: {score}")
    

if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
