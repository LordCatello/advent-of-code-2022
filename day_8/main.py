from typing import *
from enum import Enum
from collections import namedtuple
import math
from functools import reduce
import operator


INPUT_PATH = "input.txt"


Position = namedtuple("Position", "x y")
Range = namedtuple("Range", "stop step")


class Direction(Enum):
    LEFT = Position(0, -1)
    TOP = Position(-1, 0)
    RIGHT = Position(0, +1)
    BOTTOM = Position(+1, 0)


Distances = List[List[Dict[Direction, int]]]


def read_heights(filename: str) -> List[List[int]]:
    heights = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            heights.append([int(height) for height in line.strip()])

    return heights


def get_ranges(rows: int, cols: int, position: Position, direction: Direction) -> Tuple[Range, Range]:
    if direction == Direction.LEFT:
        return Range(position.x + 1, 1), Range(cols, 1)
    elif direction == Direction.RIGHT:
        return Range(position.x + 1, 1), Range(-1, -1)
    elif direction == Direction.TOP:
        return Range(rows, 1), Range(position.y + 1, 1)
    elif direction == Direction.BOTTOM:
        return Range(-1, -1), Range(position.y + 1, 1)
    else:
        raise Exception("invalid direction")


def get_positions(rows: int, cols: int, position: Position, direction: Direction) -> Iterator[Position]:
    row_range, col_range = get_ranges(rows, cols, position, direction)
    for row in range(position.x, row_range.stop, row_range.step):
        for col in range(position.y, col_range.stop, col_range.step):
            yield Position(row, col)


def compute_distance(position_a: Position, position_b: Position) -> int:
    return int(math.sqrt((position_a.x - position_b.x)**2 + (position_a.y - position_b.y)**2))


def compute_distances_line(heights: List[List[int]], start_position: Position,
                           direction: Direction, distances: Distances) -> None:
    stack = []
    rows, cols = len(heights), len(heights[0])
    #print(rows, cols, direction)
    for position in get_positions(rows, cols, start_position, direction):
        while len(stack) > 0 and heights[stack[-1].x][stack[-1].y] < heights[position.x][position.y]:
            stack.pop()

        # compute distance
        distance = compute_distance(start_position, position)
        if len(stack) > 0:
            distance = compute_distance(stack[-1], position)
        #print(position)
        distances[position.x][position.y][direction] = distance

        stack.append(position)


def compute_distances(heights: List[List[int]]) -> Distances:
    rows, cols = len(heights), len(heights[0])

    # init distances
    distances = []
    for _ in range(rows):
        distances.append([])
        for _ in range(cols):
            distances[-1].append({})

    # compute distances for all the directions
    for row in range(rows):
        compute_distances_line(heights, Position(row, 0), Direction.LEFT, distances)
        compute_distances_line(heights, Position(row, cols - 1), Direction.RIGHT, distances)
    for col in range(cols):
        compute_distances_line(heights, Position(0, col), Direction.TOP, distances)
        compute_distances_line(heights, Position(rows - 1, col), Direction.BOTTOM, distances)

    return distances


def is_on_edge(rows: int, cols: int, position: Position) -> bool:
    if position.x == 0 or position.x == rows - 1 or position.y == 0 or position.y == cols - 1:
        return True
    return False


def compute_start_point(rows, cols, position: Position, direction: Direction) -> Position:
    if direction == Direction.LEFT:
        return Position(position.x, 0)
    elif direction == Direction.RIGHT:
        return Position(position.x, cols - 1)
    elif direction == Direction.TOP:
        return Position(0, position.y)
    elif direction == Direction.BOTTOM:
        return Position(rows - 1, position.y)
    else:
        raise Exception("invalid direction")


def is_visible(position: Position, heights: List[List[int]], distance: Dict[Direction, int]) -> bool:
    rows, cols = len(heights), len(heights[0])
    if is_on_edge(rows, cols, position):
        return True

    for direction, value in distance.items():
        start_point = compute_start_point(rows, cols, position, direction)
        points_dist = compute_distance(start_point, position)
        if value == points_dist and heights[position.x][position.y] > heights[start_point.x][start_point.y]:
            return True

    return False


def solve_part_one(filename: str):
    heights = read_heights(filename)
    distances = compute_distances(heights)

    rows, cols = len(heights), len(heights[0])
    count = 0
    for row in range(rows):
        for col in range(cols):
            if is_visible(Position(row, col), heights, distances[row][col]):
                count += 1

    return count


def solve_part_two(filename: str):
    heights = read_heights(filename)
    distances = compute_distances(heights)


    # compute scenic score
    max_score = 0
    rows, cols = len(heights), len(heights[0])
    for row in range(rows):
        for col in range(cols):
            score = reduce(operator.mul, distances[row][col].values(), 1)
            max_score = max(max_score, score)

    return max_score


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))