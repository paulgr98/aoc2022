with open('input.txt') as f:
    stream = f.read()


def find_start_of_data(stream: str):
    marker_size = 4
    for i in range(len(stream) - marker_size):
        chars = set(stream[i:i + marker_size])
        if len(chars) == marker_size:
            return i + marker_size


def find_start_of_message(stream: str):
    marker_size = 14
    for i in range(len(stream) - marker_size):
        chars = set(stream[i:i + marker_size])
        if len(chars) == marker_size:
            return i + marker_size


print(f'Start of data: {find_start_of_data(stream)}')
print(f'Start of message: {find_start_of_message(stream)}')
