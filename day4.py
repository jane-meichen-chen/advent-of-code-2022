from dataclasses import dataclass
from typing import List


class CleaningRange:
    def __init__(self, range_input: str) -> None:
        start, end = range_input.split("-")
        self.start = int(start)
        self.end = int(end)
        self.values = set(range(self.start, self.end + 1))

    def is_fully_contained_within(self, another_range: "CleaningRange") -> bool:
        return self.start >= another_range.start and self.end <= another_range.end

    def overlaps_with(self, another_range: "CleaningRange") -> bool:
        return bool(self.values.intersection(another_range.values))


@dataclass
class PairOfElves:
    first_range: CleaningRange
    second_range: CleaningRange

    @staticmethod
    def from_input(value: str):
        first_range, second_range = value.split(",")
        return PairOfElves(CleaningRange(first_range), CleaningRange(second_range))

    @property
    def need_reconsideration(self) -> bool:
        return (
            self.first_range.is_fully_contained_within(self.second_range)
            or self.second_range.is_fully_contained_within(self.first_range)
        )

    @property
    def has_overlap(self) -> bool:
        return self.first_range.overlaps_with(self.second_range)


if __name__ == "__main__":
    pair_of_elves: List[PairOfElves] = []
    with open("data/day4_input.txt") as d:
        for line in d.readlines():
            pair_of_elves.append(PairOfElves.from_input(line.replace("\n", "")))
    print(f"Challenge 1: {sum(pe.need_reconsideration for pe in pair_of_elves)}")
    print(f"Challenge 2: {sum(pe.has_overlap for pe in pair_of_elves)}")
