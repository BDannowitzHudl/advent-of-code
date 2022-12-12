"""Day 12, 2022 Advent of Code puzzle solution.

https://adventofcode.com/2022/day/12
"""
from typing import List, Dict, Optional
from copy import deepcopy
import numpy as np
import networkx as nx


def parse_heightmap(data_file: str) -> np.ndarray:
    with open(data_file, 'r') as f:
        heightmap = f.read().splitlines()

    heightmap = np.array([list(d) for d in heightmap])

    # Get the first location of the S in the array
    start_loc = np.where(heightmap == "S")
    start_loc = (start_loc[0][0], start_loc[1][0])
    end_loc = np.where(heightmap == "E")
    end_loc = (end_loc[0][0], end_loc[1][0])

    # Map a-z to 1-26 in the array
    heightmap = np.array([[ord(c) - 96 for c in d] for d in heightmap])
    
    # Just set these manually, whatever
    heightmap[start_loc] = 1
    heightmap[end_loc] = 26

    return (heightmap, start_loc, end_loc)


def create_heightgraph(heightmap):
    """Created a directed graph based on the rules of each square as a node.
    
    Create an edge if you are allowed to transition from that square to the next."""
    height, width = heightmap.shape
    G = nx.DiGraph()
    for i in range(height):
        for j in range(width):
            G.add_node((i, j), height=heightmap[(i, j)])
            neighbors = get_neighbors(heightmap, loc=(i, j))
            for n in neighbors:
                G.add_edge((i, j), n)

    return G
                

def get_neighbors(heightmap, loc) -> List[tuple]: 
    """Get a list of valid neighbors for a given location on the heightmap."""
    neighbors = []
    for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        neighbor = (loc[0] + i, loc[1] + j)
        if is_valid(heightmap, loc, neighbor):
            neighbors.append(neighbor)
    return neighbors


def is_valid(heightmap: np.array, loc: tuple, neighbor: tuple) -> bool:
    """Make sure that the proposed neighbor is well-behaved."""

    # Cannot go out of bounds
    if (
        neighbor[0] < 0 or neighbor[1] < 0 or
        neighbor[0] >= heightmap.shape[0] or neighbor[1] >= heightmap.shape[1]
    ):
        return False

    loc_val = heightmap[loc]
    neighbor_val = heightmap[neighbor]
    
    # Cannot go up more than 1
    if neighbor_val - loc_val > 1:
        return False
    
    return True


def main(data_file: str):

    heightmap, start_loc, end_loc = parse_heightmap(data_file)
    G = create_heightgraph(heightmap)
    shortest_path_length = nx.shortest_path_length(G, start_loc, end_loc)
    print(f"Part 1: {shortest_path_length}")
    
    # Find the shortest route from a spot with elevation 1
    for node in G.nodes:
        try:
            if G.nodes[node]["height"] == 1:
                distance = nx.shortest_path_length(G, node, end_loc)
                if distance < shortest_path_length:
                    shortest_path_length = distance
        except nx.NetworkXNoPath:
            # This is fine. Not all who wander are lost.
            pass
    print(f"Part 2: {shortest_path_length}")
    

if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
