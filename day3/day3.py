with open('input.txt') as f:
    data = f.read().splitlines()


def find_common_rucksack_item(items: str):
    first_comp, second_comp = items[:len(items) // 2], items[len(items) // 2:]
    common_items = list(set(first_comp).intersection(set(second_comp)))[0]
    return common_items


def calc_priority(item: str):
    """
        # a - z : 1 - 26
        # A - Z : 27 - 52
    """
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 64 + 26


def find_common_group_item(group: list):
    g1, g2, g3 = group
    common_items = list(set(g1) & set(g2) & set(g3))[0]
    return common_items


# part one
priority_sum = 0
for item in data:
    common_item = find_common_rucksack_item(item)
    priority_sum += calc_priority(common_item)

print(priority_sum)

# part two
priority_sum = 0
for i in range(0, len(data), 3):
    group = data[i:i + 3]
    common_item = find_common_group_item(group)
    priority_sum += calc_priority(common_item)

print(priority_sum)
