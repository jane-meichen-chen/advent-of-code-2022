from typing import List


class Device:
    def __init__(self) -> None:
        self.cycle_count = 0
        self.X = 1
        self.signal_history = [1]
        self._display = []

    def sprite_pixel_position(self, cycle: int) -> List[int]:
        x = self.signal_history[cycle]
        return [x - 1, x, x + 1]

    def sprite_cycle_position(self, cycle: int) -> List[int]:
        x = self.signal_history[cycle]
        return [x, x + 1, x + 2]

    def action(self, instruction: str) -> None:
        if instruction == "noop":
            self._noop()
        else:
            self._addx()
            self.X += int(instruction.split(" ")[-1])

    def _noop(self):
        self.cycle_count += 1
        self.signal_history.append(self.X)

    def _addx(self):
        self.cycle_count += 2
        self.signal_history += [self.X, self.X]

    def screen(self):
        for cycle in range(1, self.cycle_count + 1):
            if cycle % 40 in self.sprite_cycle_position(cycle):
                self._display.append("#")
            else:
                self._display.append(".")

    def display(self):
        pixels = "\n".join("".join(self._display[i-40:i]) for i in range(40, len(self._display) + 1, 40))
        print(pixels)


if __name__ == "__main__":
    device = Device()
    with open("data/day10_input.txt") as d:
        for line in d.readlines():
            device.action(line.replace("\n", ""))

    print(f"Challenge 1: {sum(device.signal_history[i] * i for i in range(20, len(device.signal_history) + 1, 40))}")
    device.screen()
    device.display()
