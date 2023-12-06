# https://adventofcode.com/2023/day/6
import re


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class ElfRace:
    def __init__(self):
        pass

    def calculated_distance(self, curr_time, time):
        time_to_travel = time - curr_time
        speed = curr_time
        distance__traveled_curr_time = time_to_travel * speed

        return distance__traveled_curr_time

    def get_number_of_way_to_win(self, time, distance):
        min_time = None
        max_time = None
        left = 1
        right = time

        while min_time is None and max_time is None:
            distance_with_min_time = self.calculated_distance(left, time)
            distance_with_max_time = self.calculated_distance(right, time)

            if distance_with_min_time > distance:
                min_time = left
            else:
                left += 1

            if distance_with_min_time > distance:
                max_time = right
            else:
                right -= 1

        return right - left

    def race_simulation(self, file_name):
        # task_1
        result_task_1 = []
        game_rules = []
        for line in FileReader().gen_file_reader(file_name):
            numbers = re.findall(r"\d+", line)
            numbers = [int(num) for num in numbers]
            game_rules.append(numbers)

        for i in range(len(game_rules[0])):
            result_task_1.append(self.get_number_of_way_to_win(game_rules[0][i], game_rules[1][i]))

        result_task_2 = []
        game_time = int("".join(map(str, game_rules[0])))
        game_max_distance = int("".join(map(str, game_rules[1])))

        result_task_2 = self.get_number_of_way_to_win(game_time, game_max_distance)

        return result_task_1, result_task_2


if __name__ == "__main__":
    print("Day 6")
    elf_race_instance = ElfRace()
    result_task_1, result_task_2 = elf_race_instance.race_simulation("day_6.txt")

    multyplication_result = 1
    for item in result_task_1:
        multyplication_result = multyplication_result * item

    print("Task 1 = ", multyplication_result)
    print("Task 2 = ", result_task_2)
