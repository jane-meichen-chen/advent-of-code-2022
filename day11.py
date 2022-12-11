import math
import re
from copy import deepcopy
from typing import List, Tuple


class Monkey:
    def __init__(self, data: str):
        self.inspected = 0

        input_value = re.match(
            r"Monkey (?P<id>[0-9]):\n"
            r"  Starting items: (?P<items>[0-9, ]+)\n"
            r"  Operation: new = (?P<operation>[ old+\-*/0-9]+)\n"
            r"  Test: divisible by (?P<factor>[0-9]+)\n"
            r"    If true: throw to monkey (?P<true_id>[0-9])\n"
            r"    If false: throw to monkey (?P<false_id>[0-9])",
            data,
        )
        self.id = input_value.group("id")
        self.items = [int(i) for i in input_value.group("items").split(", ")]
        self._operation = input_value.group("operation")
        self.testing_factor = int(input_value.group("factor"))
        self.true_id = int(input_value.group("true_id"))
        self.false_id = int(input_value.group("false_id"))

    @property
    def operation(self):
        self.inspected += 1
        return lambda old: eval(self._operation, {"old": old})

    def inspect_and_throw(self) -> Tuple[int, int]:
        item_worry_level = self.items.pop(0)
        new_worry_level = self.operation(item_worry_level)
        bored_worry_level = math.floor(new_worry_level / 3)
        if bored_worry_level % self.testing_factor == 0:
            return self.true_id, bored_worry_level
        return self.false_id, bored_worry_level

    def manageable_inspect_and_throw(self, modulo) -> Tuple[List[int], List[int]]:
        true_items, false_items = [], []
        for item_worry_level in self.items:
            new_worry_level = self.operation(item_worry_level) % modulo
            if new_worry_level % self.testing_factor == 0:
                true_items.append(new_worry_level)
            else:
                false_items.append(new_worry_level)
        self.items = []
        return true_items, false_items


class MonkeyGame:
    def __init__(self, monkeys: List[Monkey]):
        self.monkeys = sorted(monkeys, key=lambda m: m.id)

    def round(self):
        for monkey in self.monkeys:
            number_of_items = len(monkey.items)
            for _ in range(number_of_items):
                target_monkey_id, item = monkey.inspect_and_throw()
                self.monkeys[target_monkey_id].items.append(item)

    def manageable_round(self):
        super_modulo = math.prod(m.testing_factor for m in self.monkeys)
        for monkey in self.monkeys:
            true_items, false_items = monkey.manageable_inspect_and_throw(super_modulo)
            self.monkeys[monkey.true_id].items += true_items
            self.monkeys[monkey.false_id].items += false_items


if __name__ == "__main__":
    with open("data/day11_input.txt") as d:
        data = d.readlines()
    data = "".join(data)
    monkeys = [Monkey(monkey_data) for monkey_data in data.split("\n\n")]
    game = MonkeyGame(monkeys)
    game2 = deepcopy(game)

    for _ in range(20):
        game.round()

    inspections = sorted([m.inspected for m in game.monkeys], reverse=True)
    print(f"Challenge 1: {inspections[0] * inspections[1]}")

    for _ in range(10_000):
        game2.manageable_round()

    inspections2 = sorted([m.inspected for m in game2.monkeys], reverse=True)
    print(f"Challenge 2: {inspections2[0] * inspections2[1]}")
