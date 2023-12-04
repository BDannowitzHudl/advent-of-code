"""Day 17, 2022 Advent of Code puzzle solution.

https://adventofcode.com/2022/day/17
"""
from typing import List, Iterator, Tuple
from enum import Enum
from copy import deepcopy
from itertools import cycle

_WELL_WIDTH: int = 7


class TileType(Enum): 
    LINE: List[List[str]] = [["."] * 2 + ["@"] * 4 + ["."] * (_WELL_WIDTH - 6)]
    PLUS: List[List[str]] = [
        ["."] * 3 + ["@"] + ["."] * (_WELL_WIDTH - 4),
        ["."] * 2 + ["@"] * 3 + ["."] * (_WELL_WIDTH - 5),
        ["."] * 3 + ["@"] + ["."] * (_WELL_WIDTH - 4),
    ]
    ELL: List[List[str]] = [
        ["."] * 2 + ["@"] * 3 + ["."] * (_WELL_WIDTH - 5),
        ["."] * 4 + ["@"] + ["."] * (_WELL_WIDTH - 5),
        ["."] * 4 + ["@"] + ["."] * (_WELL_WIDTH - 5),
    ]
    BAR: List[List[str]] = [
        ["."] * 2 + ["@"] + ["."] * (_WELL_WIDTH - 3),
    ] * 4
    SQUARE: List[List[str]] = [
        ["."] * 2 + ["@"] * 2 + ["."] * (_WELL_WIDTH - 4),
        ["."] * 2 + ["@"] * 2 + ["."] * (_WELL_WIDTH - 4),
    ]

    def print(self) -> None:
        print("\n".join(["".join(c) for c in self.value[::-1]]))

    @property
    def height(self) -> int:
        return len(self.value)

    @property
    def n_blocks(self) -> int:
        return sum([c.count("@") for c in self.value])


class Jet(Enum):
    LEFT = "<"
    RIGHT = ">"
    
    
class Well:
    
    def __init__(
        self,
        jet_cycle: Iterator,
        tile_cycle: Iterator,
        well_width: int=7,
        init_height: int=3,
    ):
        self.jet_cycle = jet_cycle
        self.tile_cycle = tile_cycle
        self.width = well_width
        self.start_height = init_height
        self.contents: List[List[str]] = [
            ["."] * self.width for _ in range(self.start_height)
        ]
    
    def drop_tile(self):
        tile = next(self.tile_cycle)
        print(tile, tile.value, len(tile.value))
        self.init_tile(tile)
        while True:
            self.shift(next(self.jet_cycle))
            if not self.down_one(tile):
                # Replace all '@' with '#'
                self.contents = [
                    [c.replace("@", "#") for c in row] for row in self.contents
                ]
                break

    def shift(self, jet: Jet):
        if jet == Jet.LEFT:
            pass
        elif jet == Jet.RIGHT:
            pass
        else:
            raise ValueError(f"Unknown jet: {jet}")
    
    def tile_coords(self, tile: TileType) -> Tuple[Tuple[int, int]]:
        """Get all the coordinates of '@' in the well contents."""
        coords: List[Tuple[int, int]] = []
        for row_idx, row in enumerate(self.contents):
            for col_idx, col in enumerate(row):
                if col == "@":
                    coords.append((row_idx, col_idx))
                if len(coords) == tile.n_blocks:
                    return tuple(coords)

    def down_one(self, tile: TileType) -> bool:
        for row_idx, col_idx in self.tile_coords(tile):
            print(row_idx, col_idx, self.contents[row_idx][col_idx])
            if row_idx == 0:
                return False
            print(self.contents[row_idx-1][col_idx])
            if self.contents[row_idx - 1][col_idx] == "#":
                return False
        # If we're still here, it's safe to move down
        for row_idx, col_idx in self.tile_coords(tile):
            self.contents[row_idx][col_idx] = "."
            self.contents[row_idx - 1][col_idx] = "@"
        return True


    def init_tile(self, tile: TileType):
        self.contents = self.contents + deepcopy(tile.value)

    @property
    def height(self):
        return len([c for c in self.contents if "#" in c])

    def __repr__(self):
        return "\n".join(
            ["|" + "".join(c) + "|" for c in self.contents[::-1]]
        ) + "\n+" + "-" * self.width + "+"

    
def main(data_file: str) -> None:
    
    with open(data_file) as f:
        data = f.read().splitlines()[0]
        
    jets = cycle([Jet(d) for d in data])
    tile_cycle = cycle(
        [TileType.LINE, TileType.PLUS, TileType.ELL, TileType.BAR, TileType.SQUARE]
    )
    well = Well(jets, tile_cycle)

    print(well)

    for _ in range(3):
        well.drop_tile()

    print(well)
        
    print(f"Part 1: {well.height}")

    
if __name__ == "__main__":
    main("test_data.csv")
    # main("puzzle_data.csv")
