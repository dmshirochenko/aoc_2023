# https://adventofcode.com/2023/day/12

from functools import lru_cache
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class SpringsFinder:
    def __init__(self):
        pass

    @staticmethod
    @lru_cache
    def count_spring_arrangements(spring_pattern: str, broken_spring_groups: tuple, next_is_blocked: bool) -> int:
        if not broken_spring_groups:
            return 0 if "#" in spring_pattern else 1
        elif not spring_pattern:
            return 0 if sum(broken_spring_groups) else 1
        elif broken_spring_groups[0] == 0:
            return (
                SpringsFinder.count_spring_arrangements(spring_pattern[1:], broken_spring_groups[1:], False)
                if spring_pattern[0] in ["?", "."]
                else 0
            )
        elif next_is_blocked:
            if spring_pattern[0] in ["?", "#"]:
                new_group_sizes = (broken_spring_groups[0] - 1,) + broken_spring_groups[1:]
                return SpringsFinder.count_spring_arrangements(spring_pattern[1:], new_group_sizes, True)
            else:
                return 0
        elif spring_pattern[0] == "#":
            new_group_sizes = (broken_spring_groups[0] - 1,) + broken_spring_groups[1:]
            return SpringsFinder.count_spring_arrangements(spring_pattern[1:], new_group_sizes, True)
        elif spring_pattern[0] == ".":
            return SpringsFinder.count_spring_arrangements(spring_pattern[1:], broken_spring_groups, False)
        else:
            new_group_sizes = (broken_spring_groups[0] - 1,) + broken_spring_groups[1:]
            return SpringsFinder.count_spring_arrangements(
                spring_pattern[1:], broken_spring_groups, False
            ) + SpringsFinder.count_spring_arrangements(spring_pattern[1:], new_group_sizes, True)

    def get_sum_num_of_arragments(self, file_name, is_part_one=False):
        sum_of_arragments = 0

        for line in FileReader.gen_file_reader(file_name):
            templates_str, num_of_broken_springs_str = line.split()
            broken_spring_groups = tuple(map(int, num_of_broken_springs_str.split(",")))
            if is_part_one:
                sum_of_arragments += SpringsFinder.count_spring_arrangements(templates_str, broken_spring_groups, False)
            else:
                templates_str = "?".join([templates_str] * 5)
                broken_spring_groups = broken_spring_groups * 5
                sum_of_arragments += SpringsFinder.count_spring_arrangements(templates_str, broken_spring_groups, False)

        return sum_of_arragments


if __name__ == "__main__":
    print("Day 12")
    springs_finder_instance = SpringsFinder()
    sum_of_arragments_part_1 = springs_finder_instance.get_sum_num_of_arragments(
        file_name="day_12.txt", is_part_one=True
    )
    print("Task 1 = ", sum_of_arragments_part_1)
    sum_of_arragments_part_2 = springs_finder_instance.get_sum_num_of_arragments(
        file_name="day_12.txt", is_part_one=False
    )
    print("Task 2 = ", sum_of_arragments_part_2)
