import string
from dataclasses import dataclass
from typing import Set, List


def priority(item: str):
    return string.ascii_letters.index(item) + 1


@dataclass
class Rucksack:
    first_container: str
    second_container: str

    @property
    def item_need_rearranging(self) -> Set:
        return set(self.first_container).intersection(self.second_container)

    @staticmethod
    def from_string(string_input: str) -> "Rucksack":
        half_way = int(len(string_input) / 2)
        return Rucksack(string_input[:half_way], string_input[half_way:])


@dataclass
class ElfGroup:
    rucksacks: List[str]

    @property
    def badge(self) -> str:
        rucksack_1, rucksack_2, rucksack_3 = self.rucksacksday
        return set(rucksack_1).intersection(rucksack_2).intersection(rucksack_3).pop()


if __name__ == "__main__":
    sum_of_priorities = 0
    sum_of_badges = 0
    lines = []
    with open("data/day3_input.txt") as d:
        for line in d.readlines():
            rucksack = Rucksack.from_string(line.replace("\n", ""))
            sum_of_priorities += sum(priority(i) for i in rucksack.item_need_rearranging)

            lines.append(line.replace("\n", ""))
            if len(lines) == 3:
                elf_group = ElfGroup(lines)
                sum_of_badges += priority(elf_group.badge)
                lines = []
    print(f"Challenge 1: {sum_of_priorities}")
    print(f"Challenge 2: {sum_of_badges}")
