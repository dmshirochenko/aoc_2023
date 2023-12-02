# https://adventofcode.com/2023/day/2
import re


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class ElfGame:
    def __init__(self):
        self.game_rules = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }

    def is_game_possible(self, game_lst):
        is_possible = True
        for game in game_lst:
            game_pairs = re.findall(r"(\d+) (green|blue|red)", game)
            for value, color in game_pairs:
                if int(value) > self.game_rules[color]:
                    is_possible = False
                    return is_possible

        return is_possible

    def min_cubes_to_play(self, game_lst):
        min_cubes = {
            "red": 1,
            "green": 1,
            "blue": 1,
        }
        for game in game_lst:
            game_pairs = re.findall(r"(\d+) (green|blue|red)", game)
            for value, color in game_pairs:
                if int(value) > min_cubes[color]:
                    min_cubes[color] = int(value)
        return min_cubes

    def sum_of_possible_games(self, file_name):
        game_number = 1
        sum_of_possible_games = 0

        min_cubes_sum = 0
        for row in FileReader.gen_file_reader(file_name):
            if self.is_game_possible(row.split(";")):
                sum_of_possible_games += game_number

            min_cubes_to_play_dct = self.min_cubes_to_play(row.split(";"))

            game_min_cubes_power = 1
            for value in min_cubes_to_play_dct.values():
                game_min_cubes_power = game_min_cubes_power * value

            min_cubes_sum += game_min_cubes_power
            game_number += 1

        return sum_of_possible_games, min_cubes_sum


if __name__ == "__main__":
    elf_game_instance = ElfGame()
    sum_of_possible_games_value, min_cubes_to_play_sum = elf_game_instance.sum_of_possible_games("day_2.txt")
    print("Task 1 = ", sum_of_possible_games_value)
    print("Task 2 = ", min_cubes_to_play_sum)
