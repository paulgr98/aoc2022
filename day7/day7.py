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


# def get_dir_sizes(commands: list):
#     """
#     Sum all file sizes in a directory,
#     add the directory as a key to a dict
#     and its size as a value.
#     Return the dict.
#
#     Commands statr with $ ('$ ls', '$ cd abc')
#     Directories are shown as [dir name] (dir abc)
#     Files are shown as [size filename] (1234 abc.txt)
#
#     Returns a dict of directory names and their sizes. ({'/': 1234, '/abc': 2345, '/abc/def': 3456})
#
#     sample input:
#     $ cd cmjgvh
#     $ ls
#     dir hdh
#     134565 hdh.sjv
#     dir hgrpfmt
#     282147 mjtq.ffd
#     42343 rvmzv.rtb
#     dir sjgvbd
#     31468 wgtjmb.thf
#     $ cd hdh
#     $ ls
#     267125 htplc.gdw
#     $ cd ..
#     $ cd hgrpfmt
#     $ ls
#     39132 lndwz
#     280595 rffmsvdw
#     """
#     dir_sizes = dict()
#     dir_stack = []
#     dirs_inside = dict()
#     current_dir = ''
#     for cmd in commands:
#         if cmd.startswith('$ cd') and '.. ' not in cmd:
#             current_dir = cmd.split(' ')[-1]
#             dir_stack.append(current_dir)
#             if current_dir not in dir_sizes:
#                 dir_sizes[current_dir] = 0
#             if current_dir not in dirs_inside:
#                 dirs_inside[current_dir] = []
#         elif cmd.startswith('$ cd') and '.. ' in cmd:
#             current_dir = dir_stack.pop()
#             dir_stack.append(current_dir)
#         elif cmd.startswith('dir'):
#             dirs_inside[current_dir].append(cmd.split(' ')[-1])
#         elif cmd[0].isdigit():
#             dir_sizes[current_dir] += int(cmd.split(' ')[0])
#
#     if '..' in dirs_inside:
#         del dirs_inside['..']
#
#     if '..' in dir_sizes:
#         del dir_sizes['..']
#
#     dirs_inside_copy = dict()
#     for key, value in dirs_inside.items():
#         dirs_inside_copy[key] = value.copy()
#
#     for i, direct in enumerate(reversed(dirs_inside)):
#         print(f'{i / len(dirs_inside) * 100:.2f}%')
#         for j, dir_inside in enumerate(dirs_inside[direct]):
#             percent = f'-> {j / len(dirs_inside[direct]) * 100:.2f}%'
#             print(percent)
#             dirs_inside_copy[direct].extend(dirs_inside_copy[dir_inside])
#
#     for direct in reversed(dirs_inside_copy):
#         for dir_inside in dirs_inside[direct]:
#             dir_sizes[direct] += dir_sizes[dir_inside]
#
#     print(dir_sizes)
#     print(dirs_inside_copy)
#
#     return dir_sizes


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
        dir_name = cmd[2:]
        if dir_name == '..':
            self.current_dir = self.current_dir.parent
        else:
            self.current_dir = self.current_dir.get_subdir(dir_name)


# sizes = get_dir_sizes(data)
# # print(sizes)
#
# total_size = 0
# for size in sizes.values():
#     if size <= 100000:
#         total_size += size
#
# print()
# expected = 95437
# if total_size == expected:
#     print('Correct!')
# else:
#     print('Incorrect!')
#     print(f'Expected: {expected}, got: {total_size} ({expected - total_size} difference)')
#
# print(total_size)

app = App()
app.get_dir_sizes(data)
print(app.home_dir.get_size())
