from queue import LifoQueue

"""
    [N]     [C]                 [Q]
    [W]     [J] [L]             [J] [V]
    [F]     [N] [D]     [L]     [S] [W]
    [R] [S] [F] [G]     [R]     [V] [Z]
    [Z] [G] [Q] [C]     [W] [C] [F] [G]
    [S] [Q] [V] [P] [S] [F] [D] [R] [S]
    [M] [P] [R] [Z] [P] [D] [N] [N] [M]
    [D] [W] [W] [F] [T] [H] [Z] [W] [R]
     1   2   3   4   5   6   7   8   9 
"""

with open('input.txt', 'r') as f:
    stack_map = f.read().splitlines()[:8]

cols = zip(*stack_map)
stack_cols = []
for col in cols:
    single_col = []
    for letter in col:
        if letter not in (' ', '[', ']'):
            single_col.append(letter)
    if single_col:
        stack_cols.append(single_col)

stack_cols = [col[::-1] for col in stack_cols]

stacks = [LifoQueue() for _ in range(9)]
stacks_copy = [LifoQueue() for _ in range(9)]

for i, col in enumerate(stack_cols):
    for letter in col:
        stacks[i].put(letter)
        stacks_copy[i].put(letter)


def move_stack_items(instruction: str, stacks: list):
    """
        move 3 from 5 to 3:
        means move the top 3 items from stack 5 to stack 3
    """
    _, num_items, _, from_stack, _, to_stack = instruction.split()
    num_items = int(num_items)
    from_stack = int(from_stack) - 1
    to_stack = int(to_stack) - 1
    for _ in range(num_items):
        to_move = stacks[from_stack].get()
        if to_move:
            stacks[to_stack].put(to_move)


def move_stack_items_at_once(instruction: str, stacks: list):
    """
        move 3 from 5 to 3:
        means move the top 3 items at once from stack 5 to stack 3.
        Moving items at once means that the items are not moved one by one,
        but all at once.
    """
    _, num_items, _, from_stack, _, to_stack = instruction.split()
    num_items = int(num_items)
    from_stack = int(from_stack) - 1
    to_stack = int(to_stack) - 1
    to_move = []
    for _ in range(num_items):
        item = stacks[from_stack].get()
        if item:
            to_move.append(item)
    to_move = to_move[::-1]
    for item in to_move:
        stacks[to_stack].put(item)


with open('input.txt', 'r') as f:
    data = f.read().splitlines()[10:]

for instruction in data:
    move_stack_items(instruction, stacks)

# part one
print("Top of each stack:")
for stack in stacks:
    print(stack.get(), end='')

print("\n")

# part two

for instruction in data:
    move_stack_items_at_once(instruction, stacks_copy)

print("Top of each stack:")
for stack in stacks_copy:
    print(stack.get(), end='')
