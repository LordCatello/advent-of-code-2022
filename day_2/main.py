INPUT_PATH = "input.txt"


SCORES = {
    ("A", "X"): 4,
    ("A", "Y"): 8,
    ("A", "Z"): 3,
    ("B", "X"): 1,
    ("B", "Y"): 5,
    ("B", "Z"): 9,
    ("C", "X"): 7,
    ("C", "Y"): 2,
    ("C", "Z"): 6
}


VALUES = {"A": 1, "B": 2, "C": 3}

WIN = {"A": "B", "B": "C", "C": "A"}
LOSE = {"A": "C", "B": "A", "C": "B"}


def solve_part_one(filename: str):
    with open(filename, "r") as f:
        score = 0

        lines = f.readlines()
        for line in lines:
            key = tuple(line.split())
            score += SCORES[key]

        return score


def solve_part_two(filename: str):
    with open(filename, "r") as f:
        score = 0

        lines = f.readlines()
        for line in lines:
            adv_play, game_status = line.split()
            if game_status == "X":
                score += VALUES[LOSE[adv_play]]
            elif game_status == "Y":
                score += VALUES[adv_play] + 3
            else:
                score += VALUES[WIN[adv_play]] + 6

        return score


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
