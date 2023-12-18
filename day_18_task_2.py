# https://adventofcode.com/2023/day/18
import heapq
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class DigPlan:
    def __init__(self):
        self.trench_coordinates = []
        self.parsed_trench_path = []
        self.move_directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
        self.direction_keys = {0: "R", 1: "D", 2: "L", 3: "U"}

    def hex_to_decimal(self, hex_string):
        return int(hex_string.strip("()").replace("#", "0x")[:7], 0)

    def convert_hex_path_to_directions(self):
        for path_element in self.trench_coordinates:
            direction = self.direction_keys[int(path_element[2][-2])]
            length = self.hex_to_decimal(path_element[2])
            self.parsed_trench_path.append([direction, length])

    def calculate_shoelace_area(self, points):
        area = 0
        for (y1, x1), (y2, x2) in zip(points, points[1:] + [points[0]]):
            area += x1 * y2 - x2 * y1
        return area / 2

    def calculate_area_from_commands(self, commands):
        y, x = 0, 0
        points = [(y, x)]
        for direction, length in commands:
            dy, dx = self.move_directions[direction]
            y += dy * length
            x += dx * length
            points.append((y, x))
        return int(self.calculate_shoelace_area(points) + sum(length for _, length in commands) / 2 + 1)

    def calculate_cubic_meters_held(self, file_name):
        for line in FileReader().gen_file_reader(file_name):
            self.trench_coordinates.append(line.split())

        self.convert_hex_path_to_directions()
        cubic_meters_held = self.calculate_area_from_commands(self.parsed_trench_path)
        return cubic_meters_held


if __name__ == "__main__":
    print("Day 18")
    dig_plan_instance = DigPlan()
    cubic_meters_held = dig_plan_instance.calculate_cubic_meters_held("day_18.txt")
    print("Task 2 is = ", cubic_meters_held)
