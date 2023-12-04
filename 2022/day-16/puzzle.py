"""Day 15, 2022 Advent of Code puzzle solution.

https://adventofcode.com/2022/day/15
"""
from typing import List
from enum import Enum
import re
from itertools import product



class Scan(Enum):
    SENSOR = "S"
    BEACON = "B"
    EXCLUDED = "#"
    NOT_EXCLUDED = "."
    

class Cave:

    def __init__(self, data, part=1) -> None:
        self.sensors: List[Sensor] = []
        self.parse_sensors(data, part=part)

    def __repr__(self):
        cave_str = ""
        for x in range(self.grid.shape[0]):
            cave_str += f"{x:02d} {''.join(list(self.grid[x, :]))}\n"
        return cave_str

    def scan(self, x, y):
        result = Scan.NOT_EXCLUDED.value
        for sensor in self.sensors:
            if (x, y) == sensor.position:
                return Scan.SENSOR.value
            elif (x, y) == sensor.beacon:
                return Scan.BEACON.value
        
        # Okay, it's not a sensor or a beacon, now:
        for sensor in self.sensors:
            if sensor.distance(x, y) <= sensor.distance(*sensor.beacon):
                return Scan.EXCLUDED.value

        return result

    def parse_sensors(self, data: List[str], part: int = 1):
        for line in data:
            # Format is:
            # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            # Capture the x and y coordinates of the sensor and beacon
            sx, sy, bx, by = re.findall(r"-?\d+", line)
            self.sensors.append(Sensor(int(sx), int(sy), int(bx), int(by)))

    def scan_row(self, row: int, buffer: int = 10_000):
        """Brute-force check the row."""
        min_x = min([s.min_x for s in self.sensors]) - buffer
        max_x = max([s.max_x for s in self.sensors]) + buffer
        excluded_count = 0
        for col in range(min_x, max_x):
            if self.scan(col, row) == Scan.EXCLUDED.value:
                excluded_count += 1

        return excluded_count

    def scan_grid(self, min_val: int = 0, max_val: int = 4_000_000):
        """Assume that there's only one cell that's not excluded.

        Then, it must be just outside the edge of the rhombus cleared
        by a sensor.
        
        Find the edges of each rhombus and scan the cells just outside
        of that edge.  The first cell that's not excluded is the answer.
        
        """
        for sensor in self.sensors:
            x = sensor.x - (sensor.beacon_distance + 1)
            y = sensor.y
            for i, xi in enumerate(range(x, x+sensor.beacon_distance+1)):
                # Edge from left to top
                if (
                    min_val <= xi <= max_val and
                    min_val <= y+i <= max_val and
                    self.scan(xi, y+i) == Scan.NOT_EXCLUDED.value
                ):
                    return xi*4_000_000 + y+i
                # Edge from left to bottom
                if (
                    min_val <= xi <= max_val and
                    min_val <= y-i <= max_val and
                    self.scan(xi, y-i) == Scan.NOT_EXCLUDED.value
                ):
                        return xi*4_000_000 + y-i
            for i, xi in enumerate(range(sensor.x, sensor.x+sensor.beacon_distance+1)):
                # Edge from right to top
                if (
                    min_val <= xi <= max_val and
                    min_val <= y+i <= max_val and
                    self.scan(xi, y+i) == Scan.NOT_EXCLUDED.value
                ):
                    return xi*4_000_000 + y+1
                # Edge from right to bottom
                if (
                    min_val <= xi <= max_val and
                    min_val <= y-i <= max_val and
                    self.scan(xi, y-i) == Scan.NOT_EXCLUDED.value
                ):
                    return xi*4_000_000 + y-i

        return None
                

class Sensor:
    
    def __init__(self, x, y, bx, by):
        self.x = x
        self.y = y
        self.bx = bx
        self.by = by
        self.beacon_distance = abs(bx - x) + abs(by - y)

    @property
    def min_x(self):
        return min(self.x, self.bx)

    @property
    def min_y(self):
        return min(self.y, self.by)
    
    @property
    def max_x(self):
        return max(self.x, self.bx)
    
    @property
    def max_y(self):
        return max(self.y, self.by)

    @property
    def position(self):
        return (self.x, self.y)
    
    @property
    def beacon(self):
        return (self.bx, self.by)

    def distance(self, x, y):
        return abs(x - self.x) + abs(y - self.y)


def main(data_file: str):

    with open(data_file, 'r') as f:
        data = f.read().splitlines()
    
    cave = Cave(data, part=1)
    n_excluded = cave.scan_row(row=2_000_000, buffer=1_000_000)
    print(f"Part 1: {n_excluded}")

    frequency = cave.scan_grid(min_val=0, max_val=4_000_000)
    print(f"Part 2: {frequency}")
    
    
if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
