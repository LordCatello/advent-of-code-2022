from typing import *


INPUT_PATH = "input.txt"


def read_input(filename: str) -> List[Optional[int]]:
    with open(filename, "r") as f:
        values = []

        instructions = f.readlines()
        for instruction in instructions:
            if instruction[0] == "n":
                values.append(None)
            else:
                values.append(int(instruction.split()[1]))

        return values


def compute_cpu_values(values: List[int]) -> List[int]:
    cpu_values = []
    next_value = 1
    for value in values:
        cpu_values.append(next_value)
        if value is not None:
            cpu_values.append(next_value)
            next_value += value
    cpu_values.append(next_value)

    return cpu_values


def solve_part_one(filename: str):
    values = read_input(filename)
    #print(values)
    cpu_values = compute_cpu_values(values)
    #print(cpu_values)

    total_sum = 0
    indexes = [19, 59, 99, 139, 179, 219]
    for index in indexes:
        total_sum += cpu_values[index] * (index + 1)
    return total_sum


def solve_part_two(filename: str):
    values = read_input(filename)
    cpu_values = compute_cpu_values(values)

    # draw
    pixel_to_draw = 0
    for i in range(240):
        if (pixel_to_draw % 40) == 0:
            pixel_to_draw = 0
            print("")
        if (cpu_values[i] - 1) <= pixel_to_draw <= (cpu_values[i] + 1):
            print("#", end="")
        else:
            print(".", end="")
        pixel_to_draw += 1


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))