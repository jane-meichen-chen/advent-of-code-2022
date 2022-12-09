from typing import List


class Forest:
    def __init__(self, value: List[str]) -> None:
        self.map: List[List[int]] = [[int(h) for h in row.replace("\n", "")] for row in value]

    def tree_height(self, x: int, y: int) -> int:
        return self.map[y][x]

    def left_to(self, x: int, y: int) -> List[int]:
        return self.map[y][:x]

    def right_to(self, x: int, y: int) -> List[int]:
        return self.map[y][x+1:]

    def top_of(self, x: int, y: int) -> List[int]:
        return [row[x] for row in self.map[:y]]

    def bottom_of(self, x: int, y: int) -> List[int]:
        return [row[x] for row in self.map[y+1:]]

    def is_visible(self, x: int, y: int) -> bool:
        """determine if the tree is visible at coordinate (x, y)"""
        def _is_visible(trees: List[int]) -> bool:
            return not trees or all(tree < self.tree_height(x, y) for tree in trees)
        return (
            _is_visible(self.left_to(x, y))
            or _is_visible(self.right_to(x, y))
            or _is_visible(self.top_of(x, y))
            or _is_visible(self.bottom_of(x, y))
        )

    def count_visible_trees(self) -> int:
        return sum(self.is_visible(x, y) for y, row in enumerate(self.map) for x, _ in enumerate(row))

    def scenic_score(self, x: int, y: int) -> int:
        def visibility(trees: List[int]) -> int:
            count = 0
            for tree in trees:
                count += 1
                if tree >= self.tree_height(x, y):
                    break
            return count
        left = self.left_to(x, y)
        left.reverse()
        right = self.right_to(x, y)
        top = self.top_of(x, y)
        top.reverse()
        bottom = self.bottom_of(x, y)
        return visibility(left) * visibility(right) * visibility(top) * visibility(bottom)

    def max_scenic_score(self):
        return max(self.scenic_score(x, y) for y, row in enumerate(self.map) for x, _ in enumerate(row))


if __name__ == "__main__":
    with open("data/day8_input.txt") as d:
        data = d.readlines()
    forest = Forest(data)
    print(f"Challenge 1: {forest.count_visible_trees()}")
    print(f"Challenge 2: {forest.max_scenic_score()}")
