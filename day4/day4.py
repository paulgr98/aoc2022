with open('input.txt', 'r') as f:
    data = f.read().splitlines()


def check_if_contains(assignments_one: set, assignments_two: set):
    return (assignments_one.issubset(assignments_two)) or (assignments_two.issubset(assignments_one))


def check_if_overlaps(assignments_one: set, assignments_two: set):
    return bool((assignments_one & assignments_two) or (assignments_two & assignments_one))


contains_sum = 0
overlaps_sum = 0
for pair in data:
    asg1, asg2 = pair.split(',')
    start_asg1, end_asg1 = asg1.split('-')
    start_asg2, end_asg2 = asg2.split('-')
    assignments1 = set(range(int(start_asg1), int(end_asg1) + 1))
    assignments2 = set(range(int(start_asg2), int(end_asg2) + 1))
    contains_sum += check_if_contains(assignments1, assignments2)
    overlaps_sum += check_if_overlaps(assignments1, assignments2)

# part one
print(contains_sum)

# part two
print(overlaps_sum)
