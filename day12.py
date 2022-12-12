import functools
import string
from typing import List, Tuple, Generator

import networkx as nx


class Map:
    def __init__(self, map_input: List[str]) -> None:
        _map = []
        for y, row in enumerate(map_input):
            _row = []
            for x, square in enumerate(row):
                if square == "S":
                    self.start = (x, y)
                    square = "a"
                if square == "E":
                    self.end = (x, y)
                    square = "z"
                _row.append(string.ascii_lowercase.index(square))
            _map.append(_row)

        self.map = _map

    def get_value(self, x: int, y: int) -> int:
        return self.map[y][x]

    def find_possible_paths(self, x: int, y: int) -> List[Tuple[int, int]]:
        possible_paths = []
        next_step_threshold = self.get_value(x, y) + 1
        if x > 0 and self.get_value(x-1, y) <= next_step_threshold:
            # ^
            possible_paths.append((x-1, y))
        if y > 0 and self.get_value(x, y-1) <= next_step_threshold:
            # <
            possible_paths.append((x, y-1))
        if x < len(self.map[0]) - 1 and self.get_value(x+1, y) <= next_step_threshold:
            # v
            possible_paths.append((x+1, y))
        if y < len(self.map) - 1 and self.get_value(x, y+1) <= next_step_threshold:
            # >
            possible_paths.append((x, y+1))
        return possible_paths

    @functools.cached_property
    def network(self) -> nx.DiGraph:
        network = nx.DiGraph()
        for y, row in enumerate(self.map):
            for x, _ in enumerate(row):
                network.add_edges_from([(x, y), next_square] for next_square in self.find_possible_paths(x, y))
        return network

    def find_shortest_path(self) -> List[Tuple[int, int]]:
        return nx.shortest_path(self.network, self.start, self.end)

    def from_any_starting_point(self) -> List[Tuple[int, int]]:
        shortest_path = None
        results = nx.single_target_shortest_path(self.network, self.end)
        for starting_node, path in results.items():
            if self.get_value(*starting_node) == 0 and (not shortest_path or len(shortest_path) > len(path)):
                shortest_path = path
        return shortest_path


if __name__ == "__main__":
    with open("data/day12_input.txt") as d:
        data = [row.replace("\n", "") for row in d.readlines()]

    height_map = Map(data)
    print(f"Challenge 1: {len(height_map.find_shortest_path()) - 1}")
    print(f"Challenge 2: {len(height_map.from_any_starting_point()) - 1}")
