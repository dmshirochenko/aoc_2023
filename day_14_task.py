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
        self.grid_matrix = []

    def calculate_sum_of_range(self, start_index, end_index):
        if start_index > end_index:
            return 0
        return (start_index + end_index) * (end_index - start_index + 1) // 2

    def compute_total_weights(self, input_file_name):
        total_sum_of_weights = 0

        for line_content in FileReader().gen_file_reader(input_file_name):
            self.grid_matrix.append([char for char in line_content])

        number_of_columns = len(self.grid_matrix[0])
        for column_index in range(number_of_columns):
            column_string = "".join(self.grid_matrix[row_index][column_index] for row_index in range(len(self.grid_matrix)))
            current_load = len(self.grid_matrix)
            for subsection in column_string.split("#"):
                rock_count_in_section = subsection.count("O")
                total_sum_of_weights += self.calculate_sum_of_range(current_load - rock_count_in_section + 1, current_load)
                current_load -= len(subsection) + 1

        return total_sum_of_weights


if __name__ == '__main__':
    print('Day 14')
    tilting_instance = DishTilting()
    sum_of_weights = tilting_instance.compute_total_weights('day_14.txt')
    print('Task 1 is = ', sum_of_weights)