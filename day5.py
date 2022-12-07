import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Crates:
    positions: Dict[str, List]

    @staticmethod
    def from_string(position: List[str]) -> "Crates":
        reversed_position = position.copy()
        reversed_position.reverse()
        stacks = {stack: [] for stack in reversed_position[0].replace(" ", "")}
        for row in reversed_position[1:]:
            for i, crate in enumerate(row):
                if re.match(r"[A-Z]", crate):
                    stacks[reversed_position[0][i]].append(crate)
        return Crates(stacks)

    def action(self, instruction: str) -> None:
        actions = re.match(
            r"move (?P<quantity>[0-9]+) from (?P<from>[0-9]) to (?P<to>[0-9])", instruction
        )
        quantity = int(actions.group("quantity"))
        from_stack = actions.group("from")
        to_stack = actions.group("to")
        moving_crates = self.positions[from_stack][-quantity:]
        moving_crates.reverse()
        self.positions[from_stack] = self.positions[from_stack][:-quantity]
        self.positions[to_stack] += moving_crates

    def action_with_new_crate_mover(self, instruction: str) -> None:
        actions = re.match(
            r"move (?P<quantity>[0-9]+) from (?P<from>[0-9]) to (?P<to>[0-9])", instruction
        )
        quantity = int(actions.group("quantity"))
        from_stack = actions.group("from")
        to_stack = actions.group("to")
        moving_crates = self.positions[from_stack][-quantity:]
        self.positions[from_stack] = self.positions[from_stack][:-quantity]
        self.positions[to_stack] += moving_crates


if __name__ == "__main__":
    crate_positions = []
    instructions = []

    instruction = False
    with open("data/day5_input.txt") as d:
        for line in d.readlines():
            if not line.replace("\n", ""):
                instruction = True
                continue

            if not instruction:
                crate_positions.append(line.replace("\n", ""))
            else:
                instructions.append(line.replace("\n", ""))

    crates_1 = Crates.from_string(crate_positions)
    crates_2 = Crates.from_string(crate_positions)
    for instruction in instructions:
        crates_1.action(instruction)
        crates_2.action_with_new_crate_mover(instruction)
    print(f"Challenge 1: {''.join(crates_1.positions[s][-1] for s in sorted(crates_1.positions.keys()))}")
    print(f"Challenge 1: {''.join(crates_2.positions[s][-1] for s in sorted(crates_2.positions.keys()))}")

