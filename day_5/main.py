from typing import *
from collections import namedtuple


INPUT_PATH = "input.txt"

Operation = namedtuple("Operation", "quantity start end")


def update_crates(crates: List[List[str]], line: str) -> None:
    for i in range(len(crates)):
        index = i * 4 + 1
        if index < len(line) and line[index] != " ":
            crates[i].append(line[index])


def get_crates_line_index(lines: List[str]) -> int:
    index = 0
    while lines[index][1] != "1":
        index += 1

    return index


def read_input(filename: str) -> Tuple[List[List[str]], List[Operation]]:
    with open(filename, "r") as f:
        lines = f.readlines()

        crates_line_index = get_crates_line_index(lines)
        crates = [[] for _ in range(len(lines[crates_line_index].split()))]

        # read crates
        for i in range(crates_line_index):
            update_crates(crates, lines[i])

        for crate in crates:
            crate.reverse()

        operations = []
        # read operations
        for i in range(crates_line_index + 2, len(lines)):
            splitted_line = lines[i].split()
            operations.append(Operation(int(splitted_line[1]), int(splitted_line[3]) - 1, int(splitted_line[5]) - 1))

    return crates, operations


def solve_part_one(filename: str):
    crates, operations = read_input(filename)

    for operation in operations:
        for _ in range(operation.quantity):
            crates[operation.end].append(crates[operation.start].pop())

    return "".join([crate[-1] for crate in crates if len(crate) > 0])


def solve_part_two(filename: str):
    crates, operations = read_input(filename)

    for operation in operations:
        end_crate = crates[operation.end]
        start_crate = crates[operation.start]
        for i in range(operation.quantity):
            end_crate.append(start_crate[len(start_crate) - operation.quantity + i])
        # pop
        for _ in range(operation.quantity):
            start_crate.pop()

    return "".join([crate[-1] for crate in crates if len(crate) > 0])


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))