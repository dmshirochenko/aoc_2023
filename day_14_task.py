# https://adventofcode.com/2023/day/14


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class DishTilting:
    def __init__(self):
        self.rocks_list = []
        self.moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.rows_count = None
        self.columns_count = None

    def calculate_sum_of_range(self, start_index, end_index):
        if start_index > end_index:
            return 0
        range_sum = (start_index + end_index) * (end_index - start_index + 1) // 2
        return range_sum

    def position_generator(self, direction):
        delta_x, delta_y = direction
        row_range = range(self.rows_count - 1, -1, -1) if delta_y == 1 else range(self.rows_count)
        column_range = range(self.columns_count - 1, -1, -1) if delta_x == 1 else range(self.columns_count)
        for row in row_range:
            for column in column_range:
                yield (column, row)

    def move_rocks(self, rocks, direction):
        delta_x, delta_y = direction
        for column, row in self.position_generator(direction):
            if rocks[row][column] == "O":
                x_position, y_position = column, row
                rocks[row][column] = "."
                while (
                    0 <= x_position < self.columns_count
                    and 0 <= y_position < self.rows_count
                    and rocks[y_position][x_position] == "."
                ):
                    x_position += delta_x
                    y_position += delta_y
                rocks[y_position - delta_y][x_position - delta_x] = "O"

        return rocks

    def get_load(self, rocks):
        total = 0
        for row, line in enumerate(rocks):
            for c in line:
                if c == "O":
                    total += self.rows_count - row
        return total

    def compute_total_weights(self, input_file_name):
        total_sum_of_weights = 0

        for line_content in FileReader().gen_file_reader(input_file_name):
            self.rocks_list.append([char for char in line_content])

        # part 1
        number_of_columns = len(self.rocks_list[0])
        for column_index in range(number_of_columns):
            column_string = "".join(
                self.rocks_list[row_index][column_index] for row_index in range(len(self.rocks_list))
            )
            current_load = len(self.rocks_list)
            for subsection in column_string.split("#"):
                rock_count_in_section = subsection.count("O")
                total_sum_of_weights += self.calculate_sum_of_range(
                    current_load - rock_count_in_section + 1, current_load
                )
                current_load -= len(subsection) + 1

        # part 2
        seen_configurations = {}
        total_weights_per_cycle = []
        current_cycle = 0
        self.rows_count = len(self.rocks_list)
        self.columns_count = len(self.rocks_list[0])

        while True:
            current_cycle += 1
            for direction in self.moves:
                self.rocks_list = self.move_rocks(self.rocks_list, direction)

            total_weight = self.get_load(self.rocks_list)
            total_weights_per_cycle.append(total_weight)

            rocks_configuration = str(self.rocks_list)
            if rocks_configuration in seen_configurations:
                cycles_since_last_seen = current_cycle - seen_configurations[rocks_configuration]
                repeating_cycle = total_weights_per_cycle[-cycles_since_last_seen:]
                cycle_index = (1000000000 - current_cycle) % cycles_since_last_seen - 1
                total_load_north = repeating_cycle[cycle_index]
                break

            seen_configurations[rocks_configuration] = current_cycle

        return total_sum_of_weights, total_load_north


if __name__ == "__main__":
    print("Day 14")
    tilting_instance = DishTilting()
    sum_of_weights, total_load_north = tilting_instance.compute_total_weights("day_14.txt")
    print("Task 1 is = ", sum_of_weights)
    print("Task 2 is = ", total_load_north)
