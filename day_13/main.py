import ast
from typing import *
from functools import cmp_to_key


INPUT_PATH = "input.txt"


def read_input(filename: str) -> List[Tuple]:
    with open(filename, "r") as f:
        lines = f.readlines()
        index = 0
        pairs = []
        while index < len(lines):
            left = ast.literal_eval(lines[index])
            right = ast.literal_eval(lines[index + 1])
            pairs.append((left, right))
            index += 3

        return pairs


def compare(left: List, right: List) -> Optional[int]:
    index = 0
    while index < len(left) and index < len(right):
        if isinstance(left[index], int) and isinstance(right[index], int):
            if left[index] < right[index]:
                return -1
            elif left[index] > right[index]:
                return 1
        elif isinstance(left[index], list) and isinstance(right[index], list):
            res = compare(left[index], right[index])
            if res != 0:
                return res
        elif isinstance(left[index], int):
            res = compare([left[index]], right[index])
            if res != 0:
                return res
        elif isinstance(right[index], int):
            res = compare(left[index], [right[index]])
            if res != 0:
                return res

        index += 1

    if index == len(left) and index == len(right):
        return 0
    elif index == len(left):
        return -1
    else:
        return 1


def solve_part_one(filename: str):
    pairs = read_input(filename)
    sum_n_ordered_pairs = 0
    for i in range(len(pairs)):
        if compare(pairs[i][0], pairs[i][1]) < 0:
            sum_n_ordered_pairs += i + 1

    return sum_n_ordered_pairs


def find(packets: List, value: List) -> int:
    for i in range(len(packets)):
        if compare(packets[i], value) == 0:
            return i


def solve_part_two(filename: str):
    pairs = read_input(filename)
    ordered_packets = []
    for pair in pairs:
        ordered_packets.append(pair[0])
        ordered_packets.append(pair[1])
    ordered_packets.append([[2]])
    ordered_packets.append([[6]])
    ordered_packets.sort(key=cmp_to_key(compare))
    index_start = find(ordered_packets, [[2]])
    index_end = find(ordered_packets, [[6]])
    return (index_start + 1) * (index_end + 1)


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))