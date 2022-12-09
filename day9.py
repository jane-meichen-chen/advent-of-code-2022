import re
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Grid:
    knots: List["Knot"]

    head_x = 0
    head_y = 0

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    def move_head(self, instruction: str):
        parsed_instruction = re.match(r"(?P<direction>[LRUD]) (?P<steps>[0-9]+)", instruction)
        direction = parsed_instruction.group("direction")
        steps = int(parsed_instruction.group("steps"))

        for _ in range(steps):
            if direction == "L":
                self.head_x -= 1
                self.min_x = min(self.min_x, self.head_x)
            if direction == "R":
                self.head_x += 1
                self.max_x = max(self.max_x, self.head_x)
            if direction == "U":
                self.head_y += 1
                self.max_y = max(self.max_y, self.head_y)
            if direction == "D":
                self.head_y -= 1
                self.min_y = min(self.min_y, self.head_y)

            prev_x, prev_y = self.head_x, self.head_y
            for knot in self.knots:
                knot.move_along_head(prev_x, prev_y)
                prev_x, prev_y = knot.x, knot.y

        self.min_x = min(self.min_x, self.head_x)
        self.max_x = max(self.max_x, self.head_x)
        self.max_y = max(self.max_y, self.head_y)
        self.min_y = min(self.min_y, self.head_y)

    def print(self):
        printable_grid = []
        for y in range(self.max_y, self.min_y - 1, -1):
            row = []
            for x in range(self.min_x, self.max_x + 1):
                if x == self.head_x and y == self.head_y:
                    row.append("H")
                else:
                    row.append(".")
                    for i, knot in enumerate(self.knots):
                        if x == self.knots[i].x and y == self.knots[i].y:
                            row[-1] = str(i+1)
                            break
            printable_grid.append(row)

        print("\n".join(" ".join(row) for row in printable_grid))
        print("============")


@dataclass
class Knot:
    x: int = 0
    y: int = 0

    travelled_coords: List[Tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        self.travelled_coords.append((0, 0))

    def move_along_head(self, prev_x, prev_y):
        if abs(prev_x - self.x) > 1 or abs(prev_y - self.y) > 1:
            diff_x = prev_x - self.x
            diff_y = prev_y - self.y

            if diff_x == 0 and abs(diff_y) == 2:
                """
                    H    H
                    . => T
                    T    .
    
                    | diff_x | = 0
                    | diff_y | = 2
                """
                self.y += int(diff_y / abs(diff_y))
            elif abs(diff_x) == 2 and diff_y == 0:
                """
                    T . H => . T H
    
                    | diff_x | = 2
                    | diff_y | = 0
                """
                self.x += int(diff_x / abs(diff_x))
            else:
                """
                    . H    . H
                    . . => . T
                    T .    . .
    
                    | diff_x | = 1
                    | diff_y | = 2
                    
                    . . H    . T H
                    T . . => . . .
    
                    | diff_x | = 2
                    | diff_y | = 1
                """
                self.x += int(diff_x / abs(diff_x))
                self.y += int(diff_y / abs(diff_y))

            self.travelled_coords.append((self.x, self.y))


if __name__ == "__main__":
    grid = Grid(knots=[Knot() for _ in range(9)])
    # grid.print()
    # grid.move_head("R 5")
    # grid.print()
    # grid.move_head("U 8")
    # grid.print()
    # grid.move_head("L 8")
    # grid.print()
    # grid.move_head("D 3")
    # grid.print()
    # grid.move_head("R 17")
    # grid.print()
    # grid.move_head("D 10")
    # grid.print()
    # grid.move_head("L 25")
    # grid.print()
    # grid.move_head("U 20")
    # grid.print()
    # print(grid.knots)

    with open("data/day9_input.txt") as d:
        for i, instruction in enumerate(d.readlines()):
            grid.move_head(instruction.replace("\n", ""))
    print(f"Challenge 1: {len(set(grid.knots[0].travelled_coords))}")
    print(f"Challenge 2: {len(set(grid.knots[-1].travelled_coords))}")
