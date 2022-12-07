from enum import Enum


class Results(Enum):
    ELF_WIN = 0
    DRAW = 3
    PLAYER_WIN = 6


class ColumnOne(Enum):
    A = "Rock"
    B = "Paper"
    C = "Scissor"

    @staticmethod
    def from_string(value: str) -> "ColumnOne":
        return ColumnOne.__getitem__(value)

    def __gt__(self, other: "ColumnTwo") -> Results:
        if self.value == other.value:
            return Results.DRAW
        if (
            (self == ColumnOne.A and other == ColumnTwo.Z)
            or (self == ColumnOne.B and other == ColumnTwo.X)
            or (self == ColumnOne.C and other == ColumnTwo.Y)
        ):
            return Results.ELF_WIN
        return Results.PLAYER_WIN


class ColumnTwo(Enum):
    X = "Rock"  # Lose
    Y = "Paper"  # Draw
    Z = "Scissor"  # Win

    @staticmethod
    def from_string(value: str) -> "ColumnTwo":
        return ColumnTwo.__getitem__(value)

    @staticmethod
    def _win(elf: ColumnOne):
        if elf == ColumnOne.A:
            return 2
        if elf == ColumnOne.B:
            return 3
        if elf == ColumnOne.C:
            return 1

    @staticmethod
    def _draw(elf: ColumnOne):
        if elf == ColumnOne.A:
            return 1
        if elf == ColumnOne.B:
            return 2
        if elf == ColumnOne.C:
            return 3

    @staticmethod
    def _lose(elf: ColumnOne):
        if elf == ColumnOne.A:
            return 3
        if elf == ColumnOne.B:
            return 1
        if elf == ColumnOne.C:
            return 2

    def play_shape_score(self, elf: ColumnOne):
        if self == ColumnTwo.X:
            return self._lose(elf)
        if self == ColumnTwo.Y:
            return self._draw(elf)
        if self == ColumnTwo.Z:
            return self._win(elf)


def calculate_result(elf: ColumnOne, player: ColumnTwo) -> int:
    """
    elf:
        A: Rock
        B: Paper
        C: Scissor
    player:
        X: Rock (1)
        Y: Paper (2)
        Z: Scissor (3)
    score:
        elf win: 0
        draw: 3
        player win: 6
    """
    shape_score = 1 if player == ColumnTwo.X else 2 if player == ColumnTwo.Y else 3
    result_score = (elf > player).value
    return shape_score + result_score


def play(elf: ColumnOne, result: ColumnTwo) -> int:
    shape_score = result.play_shape_score(elf)
    result_score = 0 if result == ColumnTwo.X else 3 if result == ColumnTwo.Y else 6
    return shape_score + result_score


if __name__ == "__main__":
    score = 0
    score2 = 0
    with open("data/day2_input.txt") as d:
        for line in d.readlines():
            elf, player = line.replace("\n", "").split(" ")
            elf = ColumnOne.from_string(elf)
            player = ColumnTwo.from_string(player)
            score += calculate_result(elf, player)
            score2 += play(elf, player)
    print(f"challenge 1: {score}")
    print(f"challenge 2: {score2}")
