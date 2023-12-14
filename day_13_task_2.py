# https://adventofcode.com/2023/day/13
from collections import deque


P = 10**9 + 7
x_ = 257


def lst_hashing(line_to_check):
    n = len(line_to_check)
    h = [0] * (n + 1)
    x = [0] * (n + 1)

    x[0] = 1
    line_to_check = " " + line_to_check

    for i in range(1, n + 1):
        h[i] = (h[i - 1] * x_ + ord(line_to_check[i])) % P
        x[i] = (x[i - 1] * x_) % P

    return h, x


def is_equal(from_1, from_2, s_len, h, x):
    return ((h[from_1 + s_len - 1] + h[from_2 - 1] * x[s_len]) % P) == (
        (h[from_2 + s_len - 1] + h[from_1 - 1] * x[s_len]) % P
    )


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class MirrorFinder:
    def __init__(self):
        pass

    def num_mistake_check(self, input_string, len_of_row, current_row_index, next_row_index):
        diff_symbols = 0
        for j in range(len_of_row):
            if input_string[current_row_index + j] != input_string[next_row_index + j]:
                diff_symbols += 1

        return diff_symbols

    def template_finder(self, template):
        is_template_found = False
        input_string, len_of_row, num_of_col = template
        h, x = lst_hashing(input_string)

        num_of_match = 1

        for i in range(0, len(input_string), len_of_row):
            current_row_index = i
            next_row_index = i + len_of_row
            not_equal_lines = 0
            if next_row_index < len(input_string):
                num_mistake_check = self.num_mistake_check(input_string, len_of_row, current_row_index, next_row_index)
                if num_mistake_check <= 1:
                    not_equal_lines = 0
                    if num_mistake_check == 1:
                        not_equal_lines += 1
                    is_template_found = True
                    matched_row_col = current_row_index // len_of_row
                    current_row_index -= len_of_row
                    next_row_index += len_of_row
                    while 0 <= current_row_index and next_row_index < num_of_col * len_of_row:
                        if not is_equal(current_row_index + 1, next_row_index + 1, len_of_row, h, x):
                            num_mistake_check = self.num_mistake_check(
                                input_string, len_of_row, current_row_index, next_row_index
                            )
                            if num_mistake_check > 1 or not_equal_lines > 1:
                                is_template_found = False
                                break
                            elif num_mistake_check == 1:
                                not_equal_lines += 1

                        current_row_index -= len_of_row
                        next_row_index += len_of_row

            if is_template_found and not_equal_lines == 1:
                break
            else:
                is_template_found = False

            num_of_match += 1

        return is_template_found, num_of_match

    def read_matrix_row_by_row(self, matrix):
        return "".join(["".join(row) for row in matrix])

    def read_matrix_column_by_column(self, matrix):
        num_rows = len(matrix)
        num_cols = len(matrix[0]) if num_rows > 0 else 0
        result = ""
        for col in range(num_cols):
            for row in range(num_rows):
                result += matrix[row][col]
        return result

    def find_mirrors(self, file_name):
        sum_of_cols_rows = 0

        dct_of_strings = {}
        num_of_template = 0
        num_of_lines = 0
        template = []
        for line in FileReader().gen_file_reader(file_name):
            if line:
                temp_list = [i for i in line]
                len_of_string = len(line)
                num_of_lines += 1
                template.append(temp_list)
            else:
                # Store the current template information in the dictionary
                dct_of_strings[num_of_template] = (template, len_of_string, num_of_lines)
                num_of_template += 1
                num_of_lines = 0
                template = []  # Reset the template

        # Store the last template if the file doesn't end with an empty line
        if template:
            dct_of_strings[num_of_template] = (template, len_of_string, num_of_lines)

        for key, item in dct_of_strings.items():
            matrix, len_of_string, num_of_lines = item
            string_row_by_row = self.read_matrix_row_by_row(matrix)
            result, index = self.template_finder((string_row_by_row, len_of_string, num_of_lines))

            if result:
                sum_of_cols_rows += 100 * index
                continue

            string_col_by_col = self.read_matrix_column_by_column(matrix)
            result, index = self.template_finder((string_col_by_col, num_of_lines, len_of_string))

            if result:
                sum_of_cols_rows += index
                continue

        return sum_of_cols_rows


if __name__ == "__main__":
    print("Day 13")
    mirror_finder_instance = MirrorFinder()
    sum_of_cols_rows = mirror_finder_instance.find_mirrors("day_13.txt")
    print("Task 2 = ", sum_of_cols_rows)
