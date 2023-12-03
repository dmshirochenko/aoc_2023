# https://adventofcode.com/2023/day/3

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class EngineFixer:
    def __init__(self, file_name):
        self.engine_schema = self._engine_shema_builder(file_name)
        self.moves = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]
        self.possible_gears = dict()

    def _engine_shema_builder(self, file_name):
        engine_schema = []
        for row in FileReader.gen_file_reader(file_name):
            temp_lst = []
            for char in row:
                temp_lst.append(char)

            engine_schema.append(temp_lst)
        return engine_schema

    def _is_move_possible(self, new_position):
        num_rows = len(self.engine_schema)
        num_cols = len(self.engine_schema[0]) if self.engine_schema else 0
        x, y = new_position
        return 0 <= x < num_rows and 0 <= y < num_cols

    def _is_parts_nearby_exist(self, num_lst):
        is_part_nerby_part_exist = False
        star_coord = ()
        num_to_add = ""
        for num, coord in num_lst:
            num_to_add += num
            x, y = coord
            for xd, yd in self.moves:
                new_coord = (x + xd, y + yd)
                if self._is_move_possible(new_coord):
                    if not self.engine_schema[x + xd][y + yd].isdigit() and self.engine_schema[x + xd][y + yd] != ".":
                        if self.engine_schema[x + xd][y + yd] == "*":  # for task 2
                            star_coord = (x + xd, y + yd)
                        is_part_nerby_part_exist = True

        int_num_to_add = int(num_to_add)
        if star_coord:
            if star_coord not in self.possible_gears:
                self.possible_gears[star_coord] = [int_num_to_add]
            else:
                self.possible_gears[star_coord].append(int_num_to_add)

        return is_part_nerby_part_exist, int_num_to_add

    def gear_calculation(self):
        gear_total = 0
        for item in self.possible_gears.values():
            if len(item) == 2:
                gear_total += item[0] * item[1]
        return gear_total

    def engine_parts_finder(self):
        sum_of_engine_parts = 0
        for i in range(len(self.engine_schema)):  # row
            right = 0
            curr = []
            while right <= len(self.engine_schema[i]):
                # we will do one extra cycle when digit is the last in the row
                if right < len(self.engine_schema[i]) and self.engine_schema[i][right].isdigit():
                    curr.append((self.engine_schema[i][right], (i, right)))
                    right += 1
                else:
                    if curr:
                        is_part_nerby_part_exist, num_to_add = self._is_parts_nearby_exist(curr)
                        if is_part_nerby_part_exist:
                            sum_of_engine_parts += num_to_add
                        curr = []
                    right += 1

        return sum_of_engine_parts


if __name__ == "__main__":
    print("Day 3")
    engine_fixer_instance = EngineFixer("day_3.txt")
    sum_of_parts = engine_fixer_instance.engine_parts_finder()
    print("Task one is = ", sum_of_parts)
    gear_total = engine_fixer_instance.gear_calculation()
    print("Task two is = ", gear_total)
