import numpy as np

def count_visible_trees(data: np.array) -> int:
    """Count how many trees are visible from the outside of the grid.
    
    A tree is visible if it is greater than all trees from it to one
    of the edges of the grid.
    
    """
    height, width = data.shape
    perimeter = (height + width) * 2 - 4
    n_visible = perimeter
    for i in range(1, height-1):
        for j in range(1, width-1):
            tree = data[i, j]
            if (
                all(tree > data[i, :j]) # Visible from the left
                or all(tree > data[i, j+1:]) # Visible from the right
                or all(tree > data[:i, j]) # Visible from the top
                or all(tree > data[i+1:, j]) # Visible from the bottom
            ):
                n_visible += 1
    return n_visible


def calculate_tree_score(data, i, j):
    """Calculate the score for a tree at (i, j).
    
    The score is the product of the number of visible trees from the
    left, right, top, and bottom.

    """
    height, width = data.shape
    tree = data[i, j]

    # Number visible from the left
    left_score = 0
    for k in np.arange(j-1, -1, -1):
        if data[i, k] >= tree:
            left_score += 1
            break
        else:
            left_score += 1

    # Number visible from the right
    right_score = 0
    for k in np.arange(j+1, width):
        if data[i, k] >= tree:
            right_score += 1
            break
        else:
            right_score += 1

    # Number visible from the top
    top_score = 0
    for k in np.arange(i-1, -1, -1):
        if data[k, j] >= tree:
            top_score += 1
            break
        else:
            top_score += 1

    # Number visible from the bottom
    bottom_score = 0
    for k in np.arange(i+1, height):
        if data[k, j] >= tree:
            bottom_score += 1
            break
        else:
            bottom_score += 1

    tree_score = (
        left_score * right_score * top_score * bottom_score
    )
    return tree_score


def calculate_highest_tree_score(data: np.array) -> int:
    height, width = data.shape
    highest_tree_score = 0
    for i in range(height):
        for j in range(width):
            tree_score = calculate_tree_score(data, i, j)
            if tree_score > highest_tree_score:
                highest_tree_score = tree_score
    return highest_tree_score
            

def main(data_file: str) -> None:
    with open(data_file, 'r') as f:
        data = f.read().splitlines()
    data = np.array([list(x) for x in data], dtype=np.int64)

    height, width = data.shape
    print(f"Forest shape: {height}x{width}")

    n_visible = count_visible_trees(data)
    print(f"Part 1: {n_visible}")

    highest_tree_score = calculate_highest_tree_score(data)
    print(f"Part 2: {highest_tree_score}")


if __name__ == "__main__":
    # main("test_data.csv")
    main("puzzle_data.csv")
    