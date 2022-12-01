with open('input.txt', 'r') as f:
    data = f.readlines()

elves = []
inventory = []
for item in data:
    if item == '\n':
        elves.append(inventory)
        inventory = []
        continue
    inventory.append(item)
elves.append(inventory)

elves = [[int(elem) for elem in items] for items in elves]

elves_sorted = sorted([sum(item) for item in elves], reverse=True)

top_3 = elves_sorted[:3]

print(top_3)

print(sum(top_3))
