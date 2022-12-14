import ast
import functools
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


class RockTraces:
    def __init__(self, trace_input: str) -> None:
        _coordinates = iter(ast.literal_eval(t) for t in trace_input.split(" -> "))
        starting_point = next(_coordinates)
        coordinates = [starting_point]

        def step(_start, _next) -> int:
            return int((_next - _start) / abs(_next - _start))

        for next_point in _coordinates:
            if starting_point[0] != next_point[0]:
                y = starting_point[1]
                direction = step(starting_point[0], next_point[0])
                coordinates += [
                    (x, y) for x in range(starting_point[0] + direction, next_point[0], direction)
                ]
            elif starting_point[1] != next_point[1]:
                x = starting_point[0]
                direction = step(starting_point[1], next_point[1])
                coordinates += [
                    (x, y) for y in range(starting_point[1] + direction, next_point[1], direction)
                ]
            coordinates.append(next_point)
            starting_point = next_point
        self.coordinates = coordinates


class StoppingPoint(Exception):
    pass


@dataclass
class Cave:
    _rocks: List[RockTraces]
    floor: bool = False
    sand_pouring_from: Tuple[int, int] = (500, 0)
    sand_coordinates: List[Tuple[int, int]] = field(default_factory=list)

    @property
    def floor_coordinate(self) -> Optional[int]:
        if self.floor:
            return self.base_max_y + 2

    @functools.cached_property
    def rock_coordinates(self) -> List[Tuple[int, int]]:
        return [rc for r in self._rocks for rc in r.coordinates]

    @functools.cached_property
    def base_min_x(self) -> int:
        return min(c[0] for c in self.rock_coordinates + self.sand_coordinates)

    @functools.cached_property
    def base_max_x(self) -> int:
        return max(c[0] for c in self.rock_coordinates + self.sand_coordinates)

    @functools.cached_property
    def base_max_y(self) -> int:
        return max(c[1] for c in self.rock_coordinates)

    def sand_movement(self, x: int, y: int) -> None:
        if not self.floor and y > self.base_max_y:
            raise StoppingPoint

        blocked = self.rock_coordinates + self.sand_coordinates
        if self.floor and y + 1 == self.floor_coordinate:
            self.sand_coordinates.append((x, y))
        elif (x, y + 1) not in blocked:
            self.sand_movement(x, y + 1)
        elif (x - 1, y + 1) not in blocked:
            self.sand_movement(x - 1, y + 1)
        elif (x + 1, y + 1) not in blocked:
            self.sand_movement(x + 1, y + 1)
        else:
            self.sand_coordinates.append((x, y))
            if self.floor and x == 500 and y == 0:
                raise StoppingPoint

    def print(self) -> None:
        rows = []
        max_y = self.base_max_y if self.floor_coordinate is None else self.floor_coordinate
        for y in range(max_y + 1):
            row = []
            for x in range(self.base_min_x, self.base_max_x + 1):
                if y == self.floor_coordinate:
                    row.append("=")
                elif x == 500 and y == 0:
                    row.append("+")
                elif (x, y) in self.rock_coordinates:
                    row.append("#")
                elif (x, y) in self.sand_coordinates:
                    row.append("o")
                else:
                    if x == 500:
                        row.append("|")
                    else:
                        row.append(".")
            if y < 10:
                rows.append(f"  {y} {''.join(row)}")
            elif y < 100:
                rows.append(f" {y} {''.join(row)}")
            else:
                rows.append(f"{y} {''.join(row)}")

        empty_space = "".join(" " for _ in range(self.base_max_x - self.base_min_x - 1))
        print("    " + str(self.base_min_x)[0] + empty_space + str(self.base_max_x)[0])
        print("    " + str(self.base_min_x)[1] + empty_space + str(self.base_max_x)[1])
        print("    " + str(self.base_min_x)[2] + empty_space + str(self.base_max_x)[2])
        print("\n".join(rows))
        print("    " + str(self.base_min_x)[0] + empty_space + str(self.base_max_x)[0])
        print("    " + str(self.base_min_x)[1] + empty_space + str(self.base_max_x)[1])
        print("    " + str(self.base_min_x)[2] + empty_space + str(self.base_max_x)[2])


if __name__ == "__main__":
    # input_data = ["498,4 -> 498,6 -> 496,6\n", "503,4 -> 502,4 -> 502,9 -> 494,9\n"]
    # cave = Cave([RockTraces(line.replace("\n", "")) for line in input_data])

    with open("data/day14_input.txt") as d:
        cave = Cave([RockTraces(line.replace("\n", "")) for line in d.readlines()])

    cave_2 = deepcopy(cave)
    cave_2.floor = True

    while True:
        try:
            cave.sand_movement(*cave.sand_pouring_from)
        except StoppingPoint:
            break

    cave.print()
    print(f"Challenge 1: {len(cave.sand_coordinates)}")

    while True:
        try:
            cave_2.sand_movement(*cave_2.sand_pouring_from)
        except StoppingPoint:
            break

    cave_2.print()
    print(f"Challenge 2: {len(set(cave_2.sand_coordinates))}")
