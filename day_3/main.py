INPUT_PATH = "input.txt"


def compute_priority(item_type: str) -> int:
    priority = ord(item_type.lower()) - ord("a") + 1
    if item_type.isupper():
        priority += 26
    return priority


def solve_part_one(filename: str):
    with open(filename, "r") as f:
        priority_sum = 0

        lines = f.readlines()
        for line in lines:
            left_set = set(line[:len(line) // 2])
            right_set = set(line[len(line)//2:])
            intersection = left_set.intersection(right_set)
            common = list(intersection)[0]
            priority_sum += compute_priority(common)

        return priority_sum


def solve_part_two(filename: str):
    with open(filename, "r") as f:
        priority_sum = 0

        lines = f.readlines()
        i = 0
        for _ in range(len(lines) // 3):
            intersection_set = set(lines[i].strip())
            i += 1
            for _ in range(2):
                intersection_set = intersection_set.intersection(set(lines[i].strip()))
                i += 1
            priority_sum += compute_priority(list(intersection_set)[0])

        return priority_sum


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
