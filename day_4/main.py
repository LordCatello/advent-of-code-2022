from typing import *


INPUT_PATH = "input.txt"


def get_pairs(lines: List[str]) -> Tuple[int, int, int, int]:
    for line in lines:
        elf_1, elf_2 = line.split(",")
        s_1, e_1 = map(int, elf_1.split("-"))
        s_2, e_2 = map(int, elf_2.split("-"))
        yield s_1, e_1, s_2, e_2


def solve_part_one(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
        count = 0

        for s_1, e_1, s_2, e_2 in get_pairs(lines):
            if (s_1 >= s_2 and e_1 <= e_2) or (s_2 >= s_1 and e_2 <= e_1):
                count += 1

        return count


def solve_part_two(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
        count = 0

        for s_1, e_1, s_2, e_2 in get_pairs(lines):
            if (e_1 >= s_2 and s_1 <= e_2) or (e_2 >= s_1 and s_2 <= e_1):
                count += 1

        return count


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
