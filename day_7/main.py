import math


INPUT_PATH = "input.txt"


MAX_SIZE = 100000
TOTAL_SPACE = 70000000
NEEDED_SPACE = 30000000


class Tree:
    def __init__(self, name: str, size: int = 0, parent: "Tree" = None):
        self.name = name
        self.size = size
        self.total_size = 0
        self.parent = parent
        self.children = {}

    def dump(self):
        if self.parent is None:
            parent_name = ""
        else:
            parent_name = self.parent.name

        print(f"name: {self.name}, size: {self.size}, total_size: {self.total_size}, parent: {parent_name}")
        for child_name, child in self.children.items():
            child.dump()


def cd(root_dir: Tree, curr_dir: Tree, dir_name: str) -> Tree:
    if dir_name == "/":
        return root_dir

    if dir_name == "..":
        return curr_dir.parent

    return curr_dir.children[dir_name]


def build_tree(filename: str) -> Tree:
    with open(filename, "r") as f:
        lines = f.readlines()

        root_dir = Tree("/")
        curr_dir = root_dir
        for line in lines:
            splitted_line = line.split()
            if splitted_line[0] == "$" and splitted_line[1] == "cd": # do nothing for ls
                curr_dir = cd(root_dir, curr_dir, splitted_line[2])
            elif splitted_line[0] != "$":
                child = Tree(splitted_line[1], 0, curr_dir)
                if splitted_line[0] != "dir":
                    child.size = int(splitted_line[0])
                    child.total_size = child.size
                curr_dir.children[splitted_line[1]] = child

        return root_dir


def update_total_size(tree: Tree):
    for child in tree.children.values():
        update_total_size(child)
        tree.total_size += child.total_size


def compute_total_size(tree: Tree, max_size: int) -> int:
    total_sum = 0
    if tree.size == 0 and tree.total_size < max_size:
        total_sum = tree.total_size

    for child in tree.children.values():
        total_sum += compute_total_size(child, max_size)

    return total_sum


def find_smallest_dir(tree: Tree, min_size: int) -> int:
    smallest_size = tree.total_size if tree.total_size >= min_size else math.inf
    for child in tree.children.values():
        if child.size == 0: # it's a dir
            smallest_size = min(smallest_size, find_smallest_dir(child, min_size))
    return smallest_size


def solve_part_one(filename: str):
    tree = build_tree(filename)
    update_total_size(tree)
    #tree.dump()
    return compute_total_size(tree, MAX_SIZE)


def solve_part_two(filename: str):#
    tree = build_tree(filename)
    update_total_size(tree)

    return find_smallest_dir(tree, NEEDED_SPACE - (TOTAL_SPACE - tree.total_size))


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
