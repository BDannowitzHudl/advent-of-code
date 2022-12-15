"""Day 13, 2022 Advent of Code puzzle solution.

https://adventofcode.com/2022/day/13
"""
from typing import List, Union, Tuple
from enum import Enum, auto
import numpy as np

SAND_ORIGIN = (0, 500)


class Material(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "O"
    ORIGIN = "+"


def make_grid(data: List[str], part: int = 1):

    # First, need to see dimensions of the cave
    min_x = 0
    max_x = 0
    min_y = np.inf
    max_y = 0
    for wall in data:
        wall = wall.split(" -> ")
        for endpoint in wall:
            y, x = endpoint.split(",")
            if int(x) > max_x:
                max_x = int(x)
            if int(y) < min_y:
                min_y = int(y)
            if int(y) > max_y:
                max_y = int(y)

    # For part two, add a big wide floor, two levels deeper
    if part == 2:
        widen = 30000
        deepen = 2
        min_y = min_y - widen
        max_y = max_y + widen
        max_x = max_x + deepen
        data = data + [f"{min_y},{max_x} -> {max_y},{max_x}"]
    
    # Initialize the grid to be all air
    grid = np.full((max_x - min_x + 1, max_y - min_y + 1), Material.AIR.value)

    # Initialize the origin of the sand
    grid[SAND_ORIGIN[0]-min_x, SAND_ORIGIN[1]-min_y] = Material.ORIGIN.value

    # Now build the rock walls
    for wall in data:
        wall = wall.split(" -> ")
        wall_start = None
        for endpoint in wall:
            y, x = endpoint.split(",")
            y, x = int(y), int(x)
            if wall_start is None:
                grid[x-min_x, y-min_y] = Material.ROCK.value
            else:
                # Fill in left-right
                y_from = min(wall_start[0], y) - min_y
                y_to = max(wall_start[0], y) - min_y + 1
                for j in range(y_from, y_to):
                    grid[x-min_x, j] = Material.ROCK.value
                # Fill in up-down
                x_from = min(wall_start[1], x) - min_x
                x_to = max(wall_start[1], x) - min_x + 1
                for i in range(x_from, x_to):
                    grid[i, y-min_y] = Material.ROCK.value
            wall_start = (y, x)

    # Return the grid, along with the bounds necessary to translate the raw coords
    return min_x, min_y, grid


class Cave:
    
    def __init__(self, data, part=1):
        self.min_x, self.min_y, self.grid = make_grid(data, part=part)
        self.n_sand = 0

    def __repr__(self):
        cave_str = ""
        for x in range(self.grid.shape[0]):
            cave_str += f"{x} {''.join(list(self.grid[x, :]))}\n"
        return cave_str

    def drop_sand(self, position=None):

        if position is None:
            position = (
                SAND_ORIGIN[0] - self.min_x,
                SAND_ORIGIN[1] - self.min_y,
            )
        
        x = position[0]
        y = position[1]

        # See if it can go down
        if self.grid[x+1, y] == Material.AIR.value:
            self.grid[x, y] = Material.AIR.value
            self.grid[x+1, y] = Material.SAND.value
            self.drop_sand((x+1, y))
        # See if it can go down-left
        elif self.grid[x+1, y-1] == Material.AIR.value:
            self.grid[x, y] = Material.AIR.value
            self.grid[x+1, y-1] = Material.SAND.value
            self.drop_sand((x+1, y-1))
        # See if it can go down-right
        elif self.grid[x+1, y+1] == Material.AIR.value:
            self.grid[x, y] = Material.AIR.value
            self.grid[x+1, y+1] = Material.SAND.value
            self.drop_sand((x+1, y+1))
        else:
            self.n_sand += 1
            # Call it a day when the sand has blocked the origin
            if position == (
                SAND_ORIGIN[0] - self.min_x,
                SAND_ORIGIN[1] - self.min_y,
            ):
                raise IndexError("Sand has blocked the origin")
        
        return


def main(data_file: str):

    with open(data_file, 'r') as f:
        data = f.read().splitlines()
    
    cave = Cave(data)
    print(cave)
    try:
        while True:
            cave.drop_sand()
    except IndexError:
        pass
    print(cave)
    print(f"Part 1: {cave.n_sand}")
    
    cave = Cave(data, part=2)
    try:
        while True:
            cave.drop_sand()
    except IndexError:
        pass
    print(f"Part 2: {cave.n_sand}")
    

if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
