"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look.
The Elves have even given you a map; on it, they've used stars to mark the top fifty
locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to
check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the
Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle
grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and
where they're even sending you ("the sky") and why your map looks mostly blank ("you
sure ask a lot of questions") and hang on did you just say the sky ("of course, where
do you think snow comes from") when you realize that the Elves are already loading you
into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document
(your puzzle input) has been amended by a very young Elf who was apparently just
excited to show off her art skills. Consequently, the Elves are having trouble reading
the values on the document.

The newly-improved calibration document consists of lines of text; each line originally
contained a specific calibration value that the Elves now need to recover. On each line,
the calibration value can be found by combining the first digit and the last digit (in
that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77.
Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration
values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

"""
from typing import List, Dict
from pathlib import Path


STR_NUMS_DICT: Dict[str, str] = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def extract_digits(line: str) -> List[str]:
    """Get the numerical digits from a string"""
    digits = []
    for char in line:
        if char.isdigit():
            digits.append(char)
    return digits


def one_line(line: str) -> int:
    """Get the numerical"""
    digits = extract_digits(line)
    return int(digits[0] + digits[-1])


def part_one(data: List[str]) -> int:
    two_digit_nums: List[int] = []
    for line in data:
        two_digit_nums.append(one_line(line))
    return sum(two_digit_nums)


def extract_digits_part_two(line: str) -> List[str]:
    """Get the numerical digits from a string"""
    digits: List[str] = []
    chars: List[str] = []
    for char in line:
        if char.isdigit():
            digits.append(char)
            chars = []
        else:
            chars.append(char)
            current_str = "".join(chars)
            for num_str, digit_str in STR_NUMS_DICT.items():
                if current_str.endswith(num_str):
                    digits.append(digit_str)
                    break
    return digits


def one_line_part_two(line: str) -> int:
    """Get the numerical"""
    digits = extract_digits_part_two(line)
    return int(digits[0] + digits[-1])


def part_two(data: List[str]) -> int:
    two_digit_nums: List[int] = []
    for line in data:
        two_digit_num = one_line_part_two(line)
        # print(line, two_digit_num)
        two_digit_nums.append(two_digit_num)
    return sum(two_digit_nums)


if __name__ == "__main__":
    # Starting at 5:17PM CST

    PART_ONE_TEST_INPUT: List[str] = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    print(part_one(PART_ONE_TEST_INPUT))

    WORKING_DIR = Path(__file__).resolve().parent
    DATA: List[str] = open(f"{WORKING_DIR}/data.csv", "r", encoding="utf-8").readlines()
    print(part_one(DATA))

    # Part 1 Complete after 5min35s (5:23PM CST)

    PART_TWO_TEST_INPUT: List[str] = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]
    print(part_two(PART_TWO_TEST_INPUT))
    print(part_two(DATA))

    # Part 2 Complete after 28min46s (5:55PM CST)
    # Small break in the middle for making dinner.
