"""Day 6, 2022 Advent of Code puzzle solution

https://adventofcode.com/2022/day/6
"""


def main(data_file: str) -> None:
    with open(data_file) as f:
        lines = [line.strip() for line in f.readlines()]
        line = lines[0]
    
    for i in range(len(line)):
        if len(set(line[i:i+4])) == 4:
            print(f"Part 1: {i+4}")
            break

    for i in range(len(line)):
        if len(set(line[i:i+14])) == 14:
            print(f"Part 2: {i+14}")
            break
    
    
if __name__ == '__main__':
    main('puzzle_data.csv')