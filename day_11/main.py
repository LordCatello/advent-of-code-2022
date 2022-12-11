from typing import *
import operator
from collections import defaultdict


INPUT_PATH = "input.txt"


class Item:
    def __init__(self, apply_mod: bool):
        self.modulo_to_value = {}
        self.apply_mod = apply_mod

    @property
    def modulo_to_value(self):
        return self._modulo_to_value

    @modulo_to_value.setter
    def modulo_to_value(self, modulo_to_value):
        self._modulo_to_value = modulo_to_value

    def get_value(self, modulo: int) -> int:
        return self.modulo_to_value[modulo]

    def set_value(self, modulo: int, value: int) -> int:
        self.modulo_to_value[modulo] = value
        if self.apply_mod:
            self.modulo_to_value[modulo] %= modulo
        return self.modulo_to_value[modulo]

    def dump(self):
        print(self.modulo_to_value)


class Monkey:
    def __init__(self, items_values: Optional[List[Item]], operation: Callable, operation_value: Optional[int],
                 boring_factor: int, test_value: int, test_dest_true: int, test_dest_false: int):
        self.items_values = items_values
        self.operation = operation
        self.operation_value = operation_value
        self.boring_factor = boring_factor
        self.test_value = test_value
        self.test_dest_true = test_dest_true
        self.test_dest_false = test_dest_false

    @property
    def items_values(self) -> List[Item]:
        return self._items_values

    @items_values.setter
    def items_values(self, items_values: Optional[ List[Item]]):
        self._items_values = items_values

    def inspect_items(self) -> List[Tuple[int, Item]]:
        monkey_to_value = []
        for i in range(len(self.items_values)):
            # update items value for each divider
            modulo_to_value = self.items_values[i].modulo_to_value
            for modulo in modulo_to_value.keys():
                operation_value = self.operation_value
                if operation_value is None:
                    operation_value = modulo_to_value[modulo]

                new_value = self.operation(modulo_to_value[modulo], operation_value) // self.boring_factor
                self.items_values[i].set_value(modulo, new_value)

            is_divisible = (self.items_values[i].get_value(self.test_value) % self.test_value) == 0
            monkey = self.test_dest_true if is_divisible else self.test_dest_false
            monkey_to_value.append((monkey, self.items_values[i]))

        self.items_values = []
        return monkey_to_value

    def add_item(self, item_value: Item) -> None:
        self.items_values.append(item_value)


def read_input(filename: str, boring_factor: int, apply_mod: bool) -> List[Monkey]:
    monkeys = []
    with open(filename, "r") as f:
        lines = f.readlines()

        index = 0
        monkey_values = []
        modulo_values = set()
        while index < len(lines):
            items_values_str = lines[index + 1].split()[2:]
            items_values = []
            for item_value_str in items_values_str:
                if item_value_str.isnumeric():
                    items_values.append(int(item_value_str))
                else:
                    items_values.append(int(item_value_str[:-1]))
            monkey_values.append(items_values)

            operation = lines[index + 2].split()[-2]
            operation = operator.add if operation == "+" else operator.mul

            operation_value = lines[index + 2].split()[-1]
            operation_value = int(operation_value) if operation_value.isnumeric() else None

            test_value = int(lines[index + 3].split()[-1])
            modulo_values.add(test_value)
            test_dest_true = int(lines[index + 4].split()[-1])
            test_dest_false = int(lines[index + 5].split()[-1])

            #print(monkey_index, items_values, operation, operation_value, test_value, test_dest_true, test_dest_false)
            monkey = Monkey([], operation, operation_value, boring_factor, test_value, test_dest_true, test_dest_false)
            monkeys.append(monkey)

            index += 7

        # create items
        for i in range(len(monkey_values)):  # for each monkey
            items = []
            for item_value in monkey_values[i]:
                item = Item(apply_mod)
                for modulo in modulo_values:
                    item.set_value(modulo, item_value)
                items.append(item)
            monkeys[i].items_values = items

    return monkeys


def compute_monkey_business(monkeys: List[Monkey], n_rounds: int) -> int:
    monkey_to_n_inspects = defaultdict(int)
    for _ in range(n_rounds):  # O(monkeys)
        for i in range(len(monkeys)):
            monkey_to_n_inspects[i] += len(monkeys[i].items_values)
            values = monkeys[i].inspect_items()  # O(items)
            for monkey_id, item_value in values:  # O(items)
                monkeys[monkey_id].add_item(item_value)

    sorted_values = sorted(monkey_to_n_inspects.values(), reverse=True)
    #print(monkey_to_n_inspects)
    return sorted_values[0] * sorted_values[1]



def solve_part_one(filename: str):
    monkeys = read_input(filename, 3, False)
    return compute_monkey_business(monkeys, 20)


def solve_part_two(filename: str):
    monkeys = read_input(filename, 1, True)
    return compute_monkey_business(monkeys, 10000)


if __name__ == "__main__":
    print("PART ONE:", solve_part_one(INPUT_PATH))
    print("PART TWO:", solve_part_two(INPUT_PATH))
