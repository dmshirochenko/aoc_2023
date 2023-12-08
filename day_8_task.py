# https://adventofcode.com/2023/day/5
import re
import math
from functools import reduce
from collections import namedtuple


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class EscapePath:
    def __init__(self):
        self.adj_lst = dict()
        self.Destination = namedtuple("Destination", "left right")
        self.nodes_that_ends_with_A = dict()

    def make_adj_lst(self, key, pair):
        pattern = r"([A-Z]{3}).*?([A-Z]{3})"
        pair_retrive = re.search(pattern, pair)
        left_dest = pair_retrive.group(1)
        right_dest = pair_retrive.group(2)

        self.adj_lst[key] = self.Destination(left_dest, right_dest)

    def lcm_of_two_numbers(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def lcm_of_list(self, numbers):
        lcm = 1
        for number in numbers:
            lcm = self.lcm_of_two_numbers(lcm, number)
        return lcm

    def get_number_of_steps_to_escape(self, file_name):
        num_of_steps_part_one = 0
        num_of_steps_part_two = 0

        file_generator = FileReader().gen_file_reader(file_name)
        moves_str = next(file_generator)
        moves_lst = [i for i in moves_str]
        _ = next(file_generator)  # skip next line

        for line in file_generator:
            key, pair = line.split(" = ")
            self.make_adj_lst(key, pair)
            if key[2] == "A":
                self.nodes_that_ends_with_A[key] = {"curr_dest": key}

        # Part 1
        curr_destination = "AAA"
        while curr_destination != "ZZZ":
            for move in moves_lst:
                if move == "L":
                    curr_destination = self.adj_lst[curr_destination].left
                elif move == "R":
                    curr_destination = self.adj_lst[curr_destination].right

                num_of_steps_part_one += 1

        # Part 2
        num_of_steps_for_each_node = []
        for key in self.nodes_that_ends_with_A.keys():
            curr_num_of_steps = 0
            is_z_node_reached = False
            while not is_z_node_reached:
                curr_destination = self.nodes_that_ends_with_A[key]["curr_dest"]
                for move in moves_lst:
                    if move == "L":
                        curr_destination = self.adj_lst[curr_destination].left

                    elif move == "R":
                        curr_destination = self.adj_lst[curr_destination].right

                    curr_num_of_steps += 1
                    self.nodes_that_ends_with_A[key]["curr_dest"] = curr_destination

                    if curr_destination[2] == "Z":
                        is_z_node_reached = True
                        num_of_steps_for_each_node.append(curr_num_of_steps)

        num_of_steps_part_two = self.lcm_of_list(num_of_steps_for_each_node)
        return num_of_steps_part_one, num_of_steps_part_two


if __name__ == "__main__":
    print("Day 8")
    escape_path_instance = EscapePath()
    num_of_steps_part_one, num_of_steps_part_two = escape_path_instance.get_number_of_steps_to_escape("day_8.txt")
    print("Task 1 =", num_of_steps_part_one)
    print("Task 2 =", num_of_steps_part_two)
