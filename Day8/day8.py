# Input contains numbers from 0 to 9 representing trees is a patch of forest.
# 0 is the shortest tree.
# 9 is the tallest tree.
# Tree is visible  if all trees between it and the edge of the grid are shorter
# We only consider trees in the same row or column as the tree in question.
# We only look up, down, left, and right from a given tree.
# All trees on the edge of the grid are visible,
# so we can just add the number of trees on the edge of the grid to the answer.

with open('input.txt') as f:
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

    return len(total_trees) + edge_trees


def find_number_of_trees_on_edges(forest: list) -> int:
    visible_trees = 0
    # Check top and bottom edges
    visible_trees += len(forest[0])
    visible_trees += len(forest[-1])
    # Check left and right edges (excluding corners)
    for row in forest[1:-1]:
        for i, col in enumerate(row):
            if i == 0 or i == len(row) - 1:
                visible_trees += 1
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
    highest_tree = max(row[1:-1])
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


# Part 2
class Tree(object):
    def __init__(self):
        self.height = -1
        self.scenic_score = -1
        self.x = -1
        self.y = -1

    def __repr__(self):
        return f'({self.x}, {self.y} -> {self.height} [{self.scenic_score}])'

    def find_scenic_score(self, forest: list):
        view_distance_right = self.find_view_distance_right(forest)
        view_distance_left = self.find_view_distance_left(forest)
        view_distance_up = self.find_view_distance_up(forest)
        view_distance_down = self.find_view_distance_down(forest)
        self.scenic_score = view_distance_left * view_distance_right * view_distance_up * view_distance_down

    def find_view_distance_right(self, forest: list) -> int:
        current_row = forest[self.x]
        view_distance = 1
        start_col = self.y + 1
        end_col = len(current_row) - 1
        for i in range(start_col, end_col):
            if current_row[i] >= self.height:
                break
            view_distance += 1
        return view_distance

    def find_view_distance_left(self, forest: list) -> int:
        current_row = forest[self.x]
        view_distance = 1
        start_col = self.y - 1
        end_col = 0
        for i in range(start_col, end_col, -1):
            if current_row[i] >= self.height:
                break
            view_distance += 1
        return view_distance

    def find_view_distance_up(self, forest: list) -> int:
        view_distance = 1
        start_row = self.x - 1
        end_row = 0
        for i in range(start_row, end_row, -1):
            if forest[i][self.y] >= self.height:
                break
            view_distance += 1
        return view_distance

    def find_view_distance_down(self, forest: list) -> int:
        view_distance = 1
        start_row = self.x + 1
        end_row = len(forest) - 1
        for i in range(start_row, end_row):
            if forest[i][self.y] >= self.height:
                break
            view_distance += 1
        return view_distance


def find_max_scenic_score(forest: list) -> int:
    trees = to_trees(forest)
    for tree in trees:
        tree.find_scenic_score(forest)

    max_scenic_score = max([tree.scenic_score for tree in trees])
    return max_scenic_score


def to_trees(forest: list[list[int]]) -> list[Tree]:
    trees = []
    for y in range(len(forest)):
        for x in range(len(forest[y])):
            tree = Tree()
            tree.height = forest[x][y]
            tree.x = x
            tree.y = y
            trees.append(tree)

    trees.sort(key=lambda t: (t.x, t.y))
    return trees


# 1470 is too low
print(f'Max scenic score: {find_max_scenic_score(data)}')
