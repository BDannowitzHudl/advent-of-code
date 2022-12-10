from enum import Enum
from typing import Optional, List
import numpy as np


class Command(Enum):
    NOOP = "noop"
    ADDX = "addx"


class Signal:
    
    def __init__(self):
        self.time_series: List[int] = [1,]
        self.image: List[str] = []

    @property
    def cycle(self) -> int:
        return (len(self.time_series) - 1) % 40

    def process(self, command: Command, value: Optional[int] = None):
        if command == Command.NOOP:
            self.process_pixel()
            self.time_series.append(self.time_series[-1])
        elif command == Command.ADDX and value is not None:
            self.process_pixel()
            self.time_series.append(self.time_series[-1])
            self.process_pixel()
            self.time_series.append(self.time_series[-1] + value)
    
    def process_pixel(self):
        if abs(self.time_series[-1] - self.cycle) < 2:
            self.image.append("#")
        else:
            self.image.append(".")
        if (self.cycle+1) % 40 == 0:
            self.image.append("\n")
        
    def calculate_score(self, positions: List[int]) -> int:
        vals = list((i) * self.time_series[i] for i in positions)
        return sum(vals)

    def render_image(self):
        print("".join(self.image))
    

def main(data_file: str):
    with open(data_file, 'r') as f:
        data = f.read().splitlines()

    signal = Signal()
    for line in data:
        cmd_list = line.split(" ")
        cmd = Command(cmd_list[0])
        value = None if len(cmd_list) == 1 else int(cmd_list[1])
        signal.process(cmd, value)

    result = signal.calculate_score(list(np.arange(20, 221, 40)))
    print(f"Part 1: {result}")

    print(f"Part 2:")
    signal.render_image()
    

if __name__ == "__main__":
    # main("test_data_small.csv")
    # main("test_data.csv")
    main("puzzle_data.csv")