from typing import *
from collections import namedtuple
from collections import deque
import math


INPUT_PATH = "input.txt"


Position = namedtuple("Position", "x y")
DIRECTIONS = [
    Position(0, 1),
    Position(0, -1),
    Position(1, 0),
    Position(-1, 0)
]


def read_input(filename: str) -> Tuple[List[List[int]], Position, Position]:
    grid = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            grid.append([])
            for char in line.strip():
                if char == "S":
                    char = "a"
                    start_position = Position(len(grid) - 1, len(grid[-1]))
                if char == "E":
                    char = "z"
                    end_position = Position(len(grid) - 1, len(grid[-1]))
                grid[-1].append(ord(char) - ord("a"))
    return grid, start_position, end_position


def get_neighbours(grid: List[List[int]], position: Position) -> Iterator[Position]:
    rows, cols = len(grid), len(grid[0])
    for direction in DIRECTIONS:
        neigh = Position(direction.x + position.x, direction.y + position.y)
        if 0 <= neigh.x < rows and 0 <= neigh.y < cols and grid[position.x][position.y] >= (grid[neigh.x][neigh.y] - 1):
            yield neigh


def compute_path_len(grid: List[List[int]], start_position: Position, end_position: Position) -> Optional[int]:
    queue = deque([start_position])
    visited = {start_position}

    distance = 0
    while len(queue) > 0:
        for _ in range(len(queue)):
            curr = queue.popleft()
            if curr == end_position:
                return distance
            for neigh in get_neighbours(grid, curr):
                if neigh not in visited:
                    visited.add(neigh)
                    queue.append(neigh)

        distance += 1

    return None


def solve_part_one(filename: str):
    grid, start_position, end_position = read_input(filename)
    return compute_path_len(grid, start_position, end_position)


def solve_part_two(filename: str):
    grid, start_position, end_position = read_input(filename)
    rows, cols = len(grid), len(grid[0])
    min_distance = math.inf
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                distance = compute_path_len(grid, Position(row, col), end_position)
                if distance is not None:
                    min_distance = min(min_distance, distance)

    return min_distance


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))