import ast
from typing import List, Optional, Union


class Packet:
    def __init__(self, signal_input: str):
        self.signal = ast.literal_eval(signal_input)

    def _compare(self, left: Union[int, List], right: Union[int, List]) -> bool:
        if isinstance(left, int):
            if isinstance(right, int):
                return None if left == right else left < right
            else:
                left = [left]

        if isinstance(right, int):
            right = [right]

        for i, _ in enumerate(left):
            try:
                right[i]
            except IndexError:
                return False

            result = self._compare(left[i], right[i])
            if result is not None:
                return result

        if len(right) > len(left):
            return True

    def is_in_order(self, right: "Packet") -> Optional[bool]:
        return self._compare(self.signal, right.signal)

    def __lt__(self, other):
        return self._compare(self.signal, other.signal)

    def __gt__(self, other):
        return self._compare(other.signal, self.signal)

    def __sub__(self, other):
        result = self._compare(self.signal, other.signal)
        return 1 if result else 0 if result is None else -1


class PairOfPacket:
    def __init__(self, signal_input: str):
        left, right = signal_input.split("\n")
        self.left = Packet(left)
        self.right = Packet(right)

    def is_in_order(self) -> bool:
        return self.left.is_in_order(self.right)


if __name__ == "__main__":
    with open("data/day13_input.txt") as d:
        data = "".join(d.readlines()).rstrip("\n")

    distress_signal = [PairOfPacket(signal) for signal in data.split("\n\n")]
    print(f"Challenge 1: {sum(i+1 for i, ds in enumerate(distress_signal) if ds.is_in_order())}")

    packets = [p.left for p in distress_signal] + [p.right for p in distress_signal]
    divider_1 = Packet("[[2]]")
    divider_2 = Packet("[[6]]")
    packets += [divider_1, divider_2]
    packets.sort()
    print(f"Challenge 2: {(packets.index(divider_1) + 1) * (packets.index(divider_2) + 1)}")
