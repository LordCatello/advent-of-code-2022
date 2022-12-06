INPUT_PATH = "input.txt"


def find_start_of_message_index(message: str, length: int) -> int:
    start = 0
    curr_char_window = set(message[start:start + length])
    while len(curr_char_window) < length:
        start += 1
        curr_char_window = set(message[start:start + length])

    return start + length


def solve_part_one(filename: str):
    with open(filename, "r") as f:
        message = f.readline()
        return find_start_of_message_index(message, 4)


def solve_part_two(filename: str):
    with open(filename, "r") as f:
        message = f.readline()
        return find_start_of_message_index(message, 14)


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))