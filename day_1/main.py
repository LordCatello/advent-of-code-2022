from heapq import heappush, heappop
from typing import *


INPUT_PATH = "input.txt"


def compute_max_calories(lines: List[str], num: int) -> List[int]:
    calories = 0
    max_calories = []

    for line in lines:
        if line == "\n":
            heappush(max_calories, calories)
            if len(max_calories) > num:
                heappop(max_calories)
            calories = 0
        else:
            calories += int(line.strip())

    return max_calories


def solve_part_one(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()

        return compute_max_calories(lines, 1)[0]


def solve_part_two(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()

        return sum(compute_max_calories(lines, 3))


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
