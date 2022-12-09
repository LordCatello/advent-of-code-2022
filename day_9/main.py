from typing import *


INPUT_PATH = "input.txt"


DIRECTIONS = {
    "L": (0, -1),
    "R": (0, +1),
    "U": (-1, 0),
    "D": (+1, 0)
}


def read_input(filename: str) -> List[Tuple[int, int]]:

    directions = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            direction, steps = line.split()
            for _ in range(int(steps)):
                directions.append(DIRECTIONS[direction])
    return directions


def compute_distance(position_a: Tuple[int, int], position_b: Tuple[int, int]) -> int:
    row_distance = abs(position_a[0] - position_b[0])
    col_distance = abs(position_a[1] - position_b[1])
    return max(row_distance, col_distance)


def compute_tail_position(head_position: Tuple[int, int], tail_position: Tuple[int, int]) -> Tuple[int, int]:
    if compute_distance(head_position, tail_position) <= 1:
        return tail_position

    # row
    row = tail_position[0]
    if tail_position[0] < head_position[0]:
        row = tail_position[0] + 1
    elif tail_position[0] > head_position[0]:
        row = tail_position[0] - 1

    # col
    col = tail_position[1]
    if tail_position[1] < head_position[1]:
        col = tail_position[1] + 1
    elif tail_position[1] > head_position[1]:
        col = tail_position[1] - 1

    return row, col


def count_positions(directions, knots: int) -> int:
    head_position, tails_positions = (0, 0), [(0, 0) for _ in range(knots)]
    visited_positions = {(0, 0)}
    for direction in directions:
        head_position = (head_position[0] + direction[0], head_position[1] + direction[1])
        prev = head_position
        for i in range(len(tails_positions)):
            tails_positions[i] = compute_tail_position(prev, tails_positions[i])
            prev = tails_positions[i]

        visited_positions.add(tails_positions[-1])

    return len(visited_positions)


def solve_part_one(filename: str):
    directions = read_input(filename)
    return count_positions(directions, 1)


def solve_part_two(filename: str):
    directions = read_input(filename)
    return count_positions(directions, 9)


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))