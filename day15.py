import itertools
import re
from multiprocessing import Process
from typing import List, Tuple, Set


def manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Sensor:
    def __init__(self, scan_result: str) -> None:
        result = re.match(
            r"Sensor at x=(?P<sensor_x>\-?[0-9]+), y=(?P<sensor_y>\-?[0-9]+):"
            r" closest beacon is at x=(?P<beacon_x>\-?[0-9]+), y=(?P<beacon_y>\-?[0-9]+)",
            scan_result
        )
        self.coordinate = (int(result.group("sensor_x")), int(result.group("sensor_y")))
        self.nearest_beacon = (int(result.group("beacon_x")), int(result.group("beacon_y")))
        self.distance = manhattan_distance(self.coordinate, self.nearest_beacon)

    def scanned_range(self, y: int) -> Tuple[int, int]:
        remaining_distance = self.distance - abs(y - self.coordinate[1])
        if remaining_distance >= 0:
            return self.coordinate[0] - remaining_distance, self.coordinate[0] + remaining_distance

    def scanned_area_within(self, x_min: int, x_max: int, y_min: int, y_max: int) -> Set[Tuple[int, int]]:
        scanned_area = set()
        min_y = max(self.coordinate[1] - self.distance, y_min)
        max_y = min(self.coordinate[1] + self.distance, y_max)
        for y in range(min_y, max_y + 1):
            lower, upper = self.scanned_range(y)
            for x in range(max(lower, x_min), min(upper, x_max) + 1):
                scanned_area.update({(x, y)})
        return scanned_area

    def covered(self, x: int, y: int) -> bool:
        return manhattan_distance(self.coordinate, (x, y)) <= self.distance


class Tunnel:
    def __init__(self, sensors: List[Sensor]) -> None:
        self.sensors = sensors
        self.min_x = min(min(s.coordinate[0], s.nearest_beacon[0]) for s in self.sensors)
        self.max_x = max(max(s.coordinate[0], s.nearest_beacon[0]) for s in self.sensors)
        self.min_y = min(min(s.coordinate[1], s.nearest_beacon[1]) for s in self.sensors)
        self.max_y = max(max(s.coordinate[1], s.nearest_beacon[1]) for s in self.sensors)

    def scanned_range_for(self, y: int) -> Set[int]:
        scanned_x = set()
        for sensor in self.sensors:
            scanned_range = sensor.scanned_range(y)
            if scanned_range:
                lower_bound, upper_bound = scanned_range
                scanned_x.update({x for x in range(lower_bound, upper_bound + 1)})
        return scanned_x


if __name__ == "__main__":
    test_case = False
    if test_case:
        input_data = [
            "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
            "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
            "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
            "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
            "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
            "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
            "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
            "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
            "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
            "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
            "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
            "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
            "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
            "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
        ]
        tunnel = Tunnel([Sensor(line) for line in input_data])
    else:
        with open("data/day15_input.txt") as d:
            tunnel = Tunnel([Sensor(line.replace("\n", "")) for line in d.readlines()])

    target_y = 10 if test_case else 2_000_000
    beacons = [s.nearest_beacon[0] for s in tunnel.sensors if s.nearest_beacon[1] == target_y]
    scanned_x = tunnel.scanned_range_for(target_y)

    print(f"Challenge 1: {len(scanned_x.difference(beacons))}")

    search_space_min = 0
    search_space_max = 20 if test_case else 4_000_000
    chunk_size = 5_000

    chunk_starts = itertools.product(
        range(search_space_min, search_space_max, chunk_size), range(search_space_min, search_space_max, chunk_size)
    )
    for x_chunk_start, y_chunk_start in chunk_starts:
        x_min = x_chunk_start
        x_max = min(x_chunk_start + chunk_size, search_space_max)
        y_min = y_chunk_start
        y_max = min(y_chunk_start + chunk_size, search_space_max)
        print(f"({x_min}, {y_min}) - ({x_max}, {y_max}):")
        searchable_area = set(itertools.product(range(x_min, x_max + 1), range(y_min, y_max + 1)))
        searched_area = set().union(*[s.scanned_area_within(x_min, x_max, y_min, y_max) for s in tunnel.sensors])
        distress_beacon = searchable_area.difference(searched_area)
        print(f"    {distress_beacon}")
        if distress_beacon:
            distress_beacon = distress_beacon.pop()
            print(f"Challenge 2: {distress_beacon[0] * 4_000_000 + distress_beacon[1]}")
            break
