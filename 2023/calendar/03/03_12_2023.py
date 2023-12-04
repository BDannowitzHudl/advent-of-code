"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will
take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not
moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise.
"Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll
still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but
nobody can figure out which one. If you can add up all the part numbers in the engine
schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the
engine. There are lots of numbers and symbols you don't really understand, but
apparently any number adjacent to a symbol, even diagonally, is a "part number" and
should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to
a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a
symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the
part numbers in the engine schematic?

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs
to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong?
Fortunately, the gondola has a phone labeled "help", so you pick it up and the
engineer answers.

Before you can explain the situation, she suggests that you look out the window.
There stands the engineer, holding a phone in one hand and waving with the other.
You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A
gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is
the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that
the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part
numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right;
its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only
adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class PartNumber:
    number: int
    row: int
    columns: List[int]

    @property
    def column_range(self) -> List[int]:
        return list(range(max(0, min(self.columns) - 1), max(self.columns) + 2))


@dataclass
class Part:
    value: str
    row: int
    column: int


class Row:
    def __init__(self, row: str, row_number: int):
        self.row = row
        self.row_number = row_number
        self.parts: List[Part] = []
        self.part_numbers: List[PartNumber] = []
        self._parse_row()

    def _parse_row(self):
        digit: List[str] = []
        digit_columns: List[int] = []
        for column, char in enumerate(self.row):
            if char.isdigit():
                digit.append(char)
                digit_columns.append(column)
            elif char != ".":
                if digit:
                    self.part_numbers.append(
                        PartNumber(
                            number=int("".join(digit)),
                            row=self.row_number,
                            columns=digit_columns,
                        )
                    )
                    digit = []
                    digit_columns = []
                self.parts.append(Part(char, self.row_number, column))
            else:
                if digit:
                    self.part_numbers.append(
                        PartNumber(int("".join(digit)), self.row_number, digit_columns)
                    )
                    digit = []
                    digit_columns = []
        if digit:
            self.part_numbers.append(
                PartNumber(int("".join(digit)), self.row_number, digit_columns)
            )
            digit = []
            digit_columns = []


class Engine:
    def __init__(self, data: List[str]):
        self.rows: Dict[int, Row] = {}
        self._parse_data(data)

    def _parse_data(self, data: List[str]):
        for row_number, row in enumerate(data):
            self.rows[row_number] = Row(row, row_number)

    @property
    def parts(self) -> List[Part]:
        parts: List[Part] = []
        for row in self.rows.values():
            parts.extend(row.parts)
        return parts

    @property
    def part_numbers(self) -> List[PartNumber]:
        part_numbers: List[PartNumber] = []
        for row in self.rows.values():
            part_numbers.extend(row.part_numbers)
        return part_numbers

    def get_row(self, row_number: int) -> Optional[Row]:
        return self.rows.get(row_number, None)

    def is_part_number(self, part_number: PartNumber) -> bool:
        # Check the row, the row above, and the row below for a part
        for row_number in range(part_number.row - 1, part_number.row + 2):
            if row := self.get_row(row_number):
                # For all parts in that row, see if it's in the column range
                for part in row.parts:
                    if part.column in part_number.column_range:
                        return True
        return False

    def evaluate(self):
        part_number_sum: int = 0
        # Evaluate every part number in the engine
        for part_number in self.part_numbers:
            if self.is_part_number(part_number):
                part_number_sum += part_number.number
        return part_number_sum

    @property
    def gears(self) -> List[Part]:
        gear_list: List[Part] = []
        for row in self.rows.values():
            for part in row.parts:
                if part.value == "*":
                    gear_list.append(part)
        return gear_list

    def gear_part_numbers(self, gear: Part) -> List[PartNumber]:
        part_number_list: List[PartNumber] = []
        for row_number in range(gear.row - 1, gear.row + 2):
            if row := self.get_row(row_number):
                for part_number in row.part_numbers:
                    if gear.column in part_number.column_range:
                        part_number_list.append(part_number)
        return part_number_list

    def gear_ratios(self) -> int:
        gear_ratio_sum: int = 0
        for gear in self.gears:
            part_number_list = self.gear_part_numbers(gear)
            if len(part_number_list) == 2:
                gear_ratio_sum += (
                    part_number_list[0].number * part_number_list[1].number
                )
        return gear_ratio_sum


def part_one(data: List[str]) -> int:
    engine = Engine(data)
    value = engine.evaluate()
    return value


def part_two(data: List[str]) -> int:
    engine = Engine(data)
    value = engine.gear_ratios()
    return value


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    TEST_DATA: List[str] = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    DATA = open(f"{WORKING_DIR}/data.csv", "r", encoding="utf-8").read().split("\n")

    # Starting Part 1 at 8:52PM CST
    # Took a break at 9:03PM CST, resuming at 9:18PM CST
    print(f"Part One (Test): {part_one(TEST_DATA)}")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part 1 at 9:43PM CST (11 + 25 = 36 minutes)

    # Starting Part 2 at 9:47PM CST
    print(f"Part Two (Test): {part_two(TEST_DATA)}")
    print(f"Part Two: {part_two(DATA)}")

    # Took a break at 9:50PM, resuming at 9:54PM CST
    # Completed Part 2 at 9:59PM CST (8 minutes)

    # Total time: 44 minutes
