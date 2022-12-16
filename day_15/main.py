from typing import *
from typing import NamedTuple
from bisect import insort


TARGET_ROW = 2000000
MAX_ROW = 4000000
FACTOR = 4000000


class Point(NamedTuple):
    row: int
    col: int


class Sensor(NamedTuple):
    point: Point
    distance: int


class Interval(NamedTuple):
    left:  int
    right: int


def compute_distance(point_a: Point, point_b: Point) -> int:
    return abs(point_a.row - point_b.row) + abs(point_a.col - point_b.col)


INPUT_PATH = "input.txt"


def read_input(filename: str) -> Tuple[List[Sensor], Set[Point]]:
    sensors, beacons = [], set()
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            splitted_line = line.split()
            beacon_point = Point(int(splitted_line[-1][2:]), int(splitted_line[-2][2:-1]))
            sensor_point = Point(int(splitted_line[3][2:-1]), int(splitted_line[2][2:-1]))
            distance = compute_distance(beacon_point, sensor_point)
            sensor = Sensor(sensor_point, distance)
            beacons.add(beacon_point)
            sensors.append(sensor)
            #print(sensor_point, beacon_point, distance)
    return sensors, beacons


def update_intervals(intervals: List[Interval], interval: Interval) -> None:
    """
    Time: O(n^2)
    Space: O(1)
    """
    insort(intervals, interval, key=lambda el: el.left)
    # adjust intervals
    index = 1
    #print(intervals)
    while index < len(intervals):
        if intervals[index].left <= intervals[index - 1].right:
            intervals[index] = Interval(intervals[index - 1].right + 1, intervals[index].right)
            if intervals[index].left > intervals[index].right:
                intervals.pop(index)
                index -= 1
        index += 1


def count_points_in_intervals(intervals: List[Interval]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    count = 0
    for interval in intervals:
        count += interval.right - interval.left + 1
    return count


def compute_intervals(sensors: List[Sensor], target_row: int) -> List[Interval]:
    intervals = []
    for sensor in sensors:
        distance = abs(sensor.point.row - target_row)
        if distance <= sensor.distance:
            distance_diff = sensor.distance - distance
            left, right = sensor.point.col - distance_diff, sensor.point.col + distance_diff
            interval = Interval(left, right)
            update_intervals(intervals, interval)
    return intervals


def compute_number_scanned_positions(sensors: List[Sensor], target_row: int) -> int:
    intervals = compute_intervals(sensors, target_row)
    return count_points_in_intervals(intervals)


def compute_number_beacons_row(beacons: Set[Point], target_row: int) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    count = 0
    for beacon in beacons:
        if beacon.row == target_row:
            count += 1
    return count


def find_candidate_col(intervals: List[Interval], min_col: int, max_col: int) -> int:
    if intervals[0].left > min_col:
        return 0
    if intervals[-1].right < max_col:
        return max_col

    for i in range(1, len(intervals)):
        if intervals[i].left != (intervals[i - 1].right + 1):
            return intervals[i - 1].right + 1


def solve_part_one(filename: str):
    sensors, beacons = read_input(filename)
    number_scanned_positions = compute_number_scanned_positions(sensors, TARGET_ROW)
    number_beacons = compute_number_beacons_row(beacons, TARGET_ROW)
    #print(number_beacons)
    return number_scanned_positions - number_beacons


def solve_part_two(filename: str):
    sensors, beacons = read_input(filename)
    for row in range(MAX_ROW + 1):
        intervals = compute_intervals(sensors, row)
        col = find_candidate_col(intervals, 0, MAX_ROW)
        if col is not None:
            #print(row, col, intervals)
            return col * FACTOR + row


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))