from typing import *
from collections import namedtuple


INPUT_PATH = "input.txt"


Position = namedtuple("Position", "x, y")
SAND_INPUT_POSITION = Position(500, 0)
DIRECTIONS = [
    Position(0, 1),
    Position(-1, 1),
    Position(1, 1)
]


def read_input(filename: str) -> Set[Position]:
    def get_position_from_str(string: str) -> Position:
        splitted_string = string.split(",")
        return Position(int(splitted_string[0]), int(splitted_string[1]))

    def update_rocks(prev: Position, curr: Position, rocks: Set[Position]) -> None:
        for row in range(min(prev.y, curr.y), max(prev.y, curr.y) + 1):
            rocks.add(Position(prev.x, row))
        for col in range(min(prev.x, curr.x), max(prev.x, curr.x) + 1):
            rocks.add(Position(col, prev.y))

    with open(filename, "r") as f:
        lines = f.readlines()
        rocks = set()
        for line in lines:
            splitted_line = line.split()
            prev = get_position_from_str(splitted_line[0])
            index = 2
            while index < len(splitted_line):
                curr = get_position_from_str(splitted_line[index])
                update_rocks(prev, curr, rocks)
                prev = curr
                index += 2

        return rocks


def is_occupied(position: Position, rocks: Set[Position], sand: Set[Position]) -> bool:
    if position in rocks or position in sand:
        return True
    return False


def compute_new_position(position: Position, rocks: Set[Position], sand: Set[Position], row_limit: Optional[int]) -> Optional[Position]:
    for i in range(len(DIRECTIONS)):
        new_pos = Position(position.x + DIRECTIONS[i].x, position.y + DIRECTIONS[i].y)
        if not is_occupied(new_pos, rocks, sand):
            if row_limit is None or new_pos.y <= row_limit:
                return new_pos
    return None


def is_outside(position: Position, last_row: int, row_limit: Optional[int]) -> bool:
    if row_limit is not None:
        last_row = row_limit
    if position.y > last_row:
        return True
    return False


def propagate_sand(rocks: Set[Position], row_limit: Optional[int] = None) -> Set[Position]:
    def propagate_one_sand() -> bool:
        """
        :return: True if the sand is in the grid
                 False otherwise
        """
        next_pos = SAND_INPUT_POSITION
        while next_pos is not None and not is_outside(next_pos, last_row, row_limit):
            prev_pos = next_pos
            next_pos = compute_new_position(prev_pos, rocks, sand, row_limit)

        if next_pos is None and prev_pos not in sand:
            sand.add(prev_pos)
            return True
        return False

    last_row = max(rocks, key=lambda el: el.y).y
    sand = set()
    while propagate_one_sand():
        pass
    return sand


def solve_part_one(filename: str):
    rocks = read_input(filename)

    sand = propagate_sand(rocks)
    return len(sand)


def solve_part_two(filename: str):
    rocks = read_input(filename)

    last_row = max(rocks, key=lambda el: el.y).y
    sand = propagate_sand(rocks, last_row + 1)
    return len(sand)


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))