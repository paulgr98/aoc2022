with open('input.txt', 'r') as f:
    data = f.read().splitlines()


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subdirs = []
        self.parent = None

    def add_file(self, file):
        self.files.append(file)

    def add_subdir(self, subdir):
        self.subdirs.append(subdir)

    def get_subdir(self, name):
        for subdir in self.subdirs:
            if subdir.name == name:
                return subdir
        return None

    def get_size(self):
        size = 0
        for file in self.files:
            size += file.size
        for subdir in self.subdirs:
            size += subdir.get_size()
        return size


class App(object):
    def __init__(self):
        self.ls_flag = False
        self.home_dir = Directory('/')
        self.current_dir = self.home_dir

    def get_dir_sizes(self, commands: list):
        for cmd in commands:
            self.handle_multi_line_cmd(cmd)
            if cmd.startswith('$ ls'):
                self.cmd_ls()
            elif cmd.startswith('$ cd'):
                self.cmd_cd(cmd)

    def handle_multi_line_cmd(self, cmd: str):
        if self.ls_flag:
            if cmd.startswith('$'):
                self.ls_flag = False
            else:
                self.handle_ls(cmd)

    def handle_ls(self, cmd: str):
        if cmd.startswith('dir'):
            self.handle_dir(cmd)
        elif cmd[0].isdigit():
            self.handle_file(cmd)

    def handle_dir(self, cmd: str):
        new_dir = Directory(cmd.split(' ')[-1])
        self.current_dir.add_subdir(new_dir)
        new_dir.parent = self.current_dir

    def handle_file(self, cmd: str):
        size = int(cmd.split(' ')[0])
        name = cmd.split(' ')[-1]
        new_file = File(name, size)
        self.current_dir.add_file(new_file)

    def cmd_ls(self):
        self.ls_flag = True

    def cmd_cd(self, cmd: str):
        dir_name = cmd[4:].strip()
        if dir_name == '/':
            self.current_dir = self.home_dir
        elif dir_name == '..':
            self.current_dir = self.current_dir.parent
        else:
            self.current_dir = self.current_dir.get_subdir(dir_name)


def get_subdirs_size_with_limit(direct: Directory, limit: int):
    total_size = 0
    for direct in direct.subdirs:
        if direct.subdirs:
            total_size += get_subdirs_size_with_limit(direct, limit)
        size = direct.get_size()
        if size <= limit:
            total_size += size
    return total_size


def get_subdirs_with_limit(direct: Directory, limit: int):
    subdirs = []
    for direct in direct.subdirs:
        if direct.subdirs:
            subdirs.extend(get_subdirs_with_limit(direct, limit))
        size = direct.get_size()
        if size <= limit:
            subdirs.append(direct)
    return subdirs


def get_dirs_sizes(direct: Directory):
    dirs_sizes = dict()
    for direct in direct.subdirs:
        if direct.subdirs:
            dirs_sizes.update(get_dirs_sizes(direct))
        dirs_sizes[direct.name] = direct.get_size()
    return dirs_sizes


def get_depth_from_home(direct: Directory):
    depth = 0
    while direct.parent:
        direct = direct.parent
        depth += 1
    return depth


def print_tree(direct: Directory):
    depth = get_depth_from_home(direct)
    dir_size = direct.get_size()
    print(f'{" - " * depth}{direct.name} ({dir_size})')
    for file in direct.files:
        print(f'{" + " * (depth + 1)}{file.name} {file.size}')
    for direct in direct.subdirs:
        print_tree(direct)


app = App()
app.get_dir_sizes(data)

total_size = app.home_dir.get_size()
total_size_with_limit = get_subdirs_size_with_limit(app.home_dir, 100000)

print(f'Total size: {total_size}')
limit_dirs = get_subdirs_with_limit(app.home_dir, 100000)

print(f'{"Correct total size" if total_size == 45174025 else "Wrong total size"}')
print(f'Total size with limit: {total_size_with_limit}')

total_size_with_limit_method2 = sum([direct.get_size() for direct in limit_dirs])

print(f'Total size with limit (method 2): {total_size_with_limit_method2}')

disk_size = 70000000
update_size = 30000000
free_space = disk_size - total_size
print(f'Free space: {free_space}')
required_space = update_size - free_space
print(f'Required additional space: {required_space}')

print()
dirs_sizes = get_dirs_sizes(app.home_dir)

dirs_sizes = {k: v for k, v in sorted(dirs_sizes.items(), key=lambda item: item[1])}
# print(dirs_sizes)


name = ''
size = 0
expected_size = 5649896
for dir_name, dir_size in dirs_sizes.items():
    if dir_size >= required_space:
        name = dir_name
        size = dir_size
        break

if size == expected_size:
    print(f'Correct! Found dir: {name} ({size})')
else:
    print(f'Incorrect! Found dir: {name} ({size})')
    print(f'Expected size: {expected_size}')
    print(f'Difference: {expected_size - size}')

print()
# print_tree(app.home_dir)
