import json


def add_directory(file, size):
    direct = {}
    line = next_line(file)

    while line[0] != "$":
        direct[line[1]] = {} if line[0] == "dir" else int(line[0])
        line = next_line(file)

    while line[2] != "..":
        if line[1] != "ls":
            direct[line[2]] = add_directory(next_line(file, True), size)

            dir_size = get_size(direct[line[2]])
            size[0] += dir_size if dir_size <= 100000 else 0

        line = next_line(file)

    return direct


def next_line(file, skip=False):
    line = file.readline().strip().split()
    return file if skip else line if line != [] else ["$", "cd", ".."]


def get_size(direct):
    size = 0
    for sub_dir in direct.values():
        size += get_size(sub_dir) if type(sub_dir) == dict else sub_dir

    return size


def find_optimal_directory(direct, size, optimal_directory):
    for name, sub_dir in direct.items():
        if type(sub_dir) == dict:
            optimal_directory = find_optimal_directory(sub_dir, size, optimal_directory)[0]
            sub_dir_size = get_size(sub_dir)

            if size < sub_dir_size < optimal_directory[0]:
                optimal_directory = [sub_dir_size, name]

    return optimal_directory, direct


if __name__ == "__main__":
    with open("input.txt") as file:
        small_dirs = [0]  # Total size of dirs <= 100000
        home = {next_line(file)[2]: add_directory(next_line(file, True), small_dirs)}
        print(json.dumps(home, indent=2))

    TOTAL_DISK_SPACE = 70000000
    MINIMUM_UNUSED_SPACE = 30000000
    home_size = get_size(home)
    print(f"Total size: {home_size}")

    space_needed = MINIMUM_UNUSED_SPACE - TOTAL_DISK_SPACE + home_size
    optimal_directory = find_optimal_directory(home, space_needed, [home_size, None])  # Size, name

    print(f"Total size with limit: {small_dirs[0]}")
    print(f"Dir to delete: {optimal_directory[0][1]} with size {optimal_directory[0][0]}")
