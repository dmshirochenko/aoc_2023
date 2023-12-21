# https://adventofcode.com/2023/day/20
from collections import deque


from scipy.optimize import curve_fit
import numpy as np


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class PolynomialExtrapolator:
    def __init__(self):
        self.coefficients = None

    @staticmethod
    def quadratic_poly(x, a, b, c):
        return a * x**2 + b * x + c

    def fit(self, x_data, y_data):
        self.coefficients, _ = curve_fit(self.quadratic_poly, x_data, y_data)

    def extrapolate(self, x, precision=None):
        if self.coefficients is None:
            raise ValueError("Polynomial not fitted yet. Call fit() first.")
        a, b, c = self.coefficients
        result = self.quadratic_poly(x, a, b, c)
        if precision is not None:
            result = round(result, precision)
        return result


class ElfJourney:
    def __init__(self):
        self.grid = []
        self.moves = {(-1, 0), (0, -1), (1, 0), (0, 1)}
        self.starting_point = None
        self.seen_tiles = set()
        self.seen_tiles_step_64 = set()

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def grid_expansion(self, max_num_steps):
        new_grid = []
        if max_num_steps > 64:
            for i in range(5):
                for line in self.grid:
                    new_grid.append(5 * line)
        else:
            new_grid = self.grid

        width = len(new_grid[0])
        height = len(new_grid)
        row_start, col_start = width // 2, height // 2

        return row_start, col_start, new_grid

    def bfs(self, max_num_steps):
        queue = deque()
        seen_tiles = set()

        row_start, col_start, grid = self.grid_expansion(max_num_steps)

        parity = max_num_steps % 2
        queue.append((row_start, col_start, 0))

        num_tiles = 0
        while queue:
            curr_row, curr_col, step = queue.popleft()
            if step > max_num_steps:
                break
            if (curr_row, curr_col) in seen_tiles:
                continue

            seen_tiles.add((curr_row, curr_col))

            if step % 2 == parity:
                num_tiles += 1

            for move in self.moves:
                row_d, col_d = move
                row_new, col_new = curr_row + row_d, curr_col + col_d
                if self.is_within_grid((row_new, col_new), grid):
                    if grid[row_new][col_new] != "#":
                        queue.append((row_new, col_new, step + 1))

        return num_tiles

    def get_num_of_tiles_elf_can_visit(self, file_name, max_dist):
        row = 0
        for line in FileReader().gen_file_reader(file_name):
            lst_to_add = []
            for col in range(len(line)):
                if line[col] == "S":
                    self.starting_point = (row, col)
                lst_to_add.append(line[col])
            self.grid.append(lst_to_add)
            row += 1

        # part 1
        row_start, col_start = self.starting_point
        step = 0
        num_of_visited_tiles_part_1 = self.bfs(max_dist)

        # part 2
        num_of_visited_tiles_part_2 = 0
        # polynomial extrapolation
        x0 = self.bfs(65)
        x1 = self.bfs(65 + 131)
        x3 = self.bfs(65 + 2 * 131)

        extrapolator = PolynomialExtrapolator()

        # Fit the model
        x_data = np.array([0, 1, 2])
        y_data = np.array([x0, x1, x3])
        extrapolator.fit(x_data, y_data)

        # Extrapolate (26501365 = 202300 * 131 + 65 where 131 is the dimension of the grid)
        n = 202300
        num_of_visited_tiles_part_2 = int(extrapolator.extrapolate(n, precision=0))
        return num_of_visited_tiles_part_1, num_of_visited_tiles_part_2


if __name__ == "__main__":
    print("Day 21")
    elf_journey_instance = ElfJourney()
    # part 1
    max_dist = 64
    num_of_tiles_visited_part_1, num_of_tiles_visited_part_2 = elf_journey_instance.get_num_of_tiles_elf_can_visit(
        "day_21.txt", max_dist
    )
    print("Task 1 is = ", num_of_tiles_visited_part_1)
    print("Task 2 is = ", num_of_tiles_visited_part_2)
