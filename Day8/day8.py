# Input contains numbers from 0 to 9 representing trees is a patch of forest.
# 0 is the shortest tree.
# 9 is the tallest tree.
# Tree is visible  if all trees between it and the edge of the grid are shorter
# We only consider trees in the same row or column as the tree in question.
# We only look up, down, left, and right from a given tree.
# All trees on the edge of the grid are visible,
# so we can just add the number of trees on the edge of the grid to the answer.

with open('test.txt') as f:
    data = [list(map(int, line.strip())) for line in f]


# Part 1
# Find the number of visible trees in the forest.
def find_number_of_visible_trees(forest: list) -> int:
    edge_trees = find_number_of_trees_on_edges(forest)
    trees_horizontally = find_trees_horizontally(forest)
    # transpose the forest
    forest_transposed = list(map(list, zip(*forest)))
    trees_vertically = find_trees_horizontally(forest_transposed)
    trees_vertically = [(y, x) for x, y in trees_vertically]
    total_trees = set(trees_horizontally + trees_vertically)
    print(sorted(total_trees))

    return len(total_trees) + edge_trees


def find_number_of_trees_on_edges(forest: list) -> int:
    visible_trees = 0
    # Check top and bottom edges
    visible_trees += len(forest[0])
    visible_trees += len(forest[-1])
    # Check left and right edges (excluding corners)
    for row in forest[1:-1]:
        visible_trees += 1 if row[0] else 0
        visible_trees += 1 if row[-1] else 0
    return visible_trees


def find_trees_horizontally(forest: list) -> list:
    trees = []
    for row in forest[1:-1]:
        left = find_trees_left_for_row_number(row, forest.index(row))
        right = find_trees_right_for_row_number(row, forest.index(row))
        total_trees = set(left + right)
        trees.extend(list(total_trees))
    return trees


def find_trees_left_for_row_number(row: list, row_number) -> list:
    visible_trees = []
    highest_tree = max(row)
    first_tree = row[0]
    for index in range(1, len(row) - 2):
        if row[index] > first_tree:
            visible_trees.append((row_number, index))
            first_tree = row[index]
        if row[index] == highest_tree:
            break
    return visible_trees


def find_trees_right_for_row_number(row: list, row_number) -> list:
    visible_trees = []
    highest_tree = max(row)
    last_tree = row[-1]
    for index in range(len(row) - 2, 0, -1):
        if row[index] > last_tree:
            visible_trees.append((row_number, index))
            last_tree = row[index]
        if row[index] == highest_tree:
            break
    return visible_trees


answer = find_number_of_visible_trees(data)
print(f'Visible trees: {answer}')
