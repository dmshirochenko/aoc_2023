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
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
        self.trench_path = []
        self.trench_coord = set()
        self.seen_outer_terrain = set()
        self.moves = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}

    def get_number_of_cells(self):
        return self.grid_size * self.grid_size

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def draw_path_on_grid(self):
        curr_node = (200, 201)
        for trench_part in self.trench_path:
            direction, num_steps, color = trench_part
            for i in range(int(num_steps)):
                curr_row, curr_col = curr_node
                row_d, col_d = self.moves[direction]

                new_row, new_col = curr_row + row_d, curr_col + col_d
                self.trench_coord.add((new_row, new_col))

                curr_node = (new_row, new_col)

    def bfs_to_find_outer_terrain(self, grid, starting_point):
        if starting_point not in self.trench_coord:
            queue = deque([starting_point])
            self.seen_outer_terrain.add(starting_point)

            while queue:
                node = queue.popleft()
                curr_row, curr_col = node
                for direction, coor_diff in self.moves.items():
                    row_diff, col_diff = coor_diff
                    new_row, new_col = curr_row + row_diff, curr_col + col_diff
                    if self.is_within_grid((new_row, new_col), self.grid):
                        if (new_row, new_col) not in self.seen_outer_terrain and (
                            new_row,
                            new_col,
                        ) not in self.trench_coord:
                            self.seen_outer_terrain.add((new_row, new_col))
                            queue.append((new_row, new_col))

    def get_num_of_cubic_metes_holds(self, file_name):
        cubic_metes_holds = 0

        for line in FileReader().gen_file_reader(file_name):
            self.trench_path.append(line.split())

        self.draw_path_on_grid()
        self.bfs_to_find_outer_terrain(self.grid, (self.grid_size - 1, self.grid_size - 1))

        total_num_of_tiles = self.get_number_of_cells()
        num_of_trench_path = len(self.trench_coord)
        num_of_empty_tiles = len(self.seen_outer_terrain)

        num_of_inner_trench = total_num_of_tiles - num_of_trench_path - num_of_empty_tiles

        cubic_metes_holds += num_of_inner_trench + num_of_trench_path

        return cubic_metes_holds


if __name__ == "__main__":
    print("Day 18")
    grid_size = 500  # could be depend on the input
    dig_plan_instance = DigPlan(grid_size)
    cubic_metes_holds = dig_plan_instance.get_num_of_cubic_metes_holds("day_18.txt")
    print("Task 1 is = ", cubic_metes_holds)
    """
    for row in range(len(dig_plan_instance.grid)):
        for col in range(len(dig_plan_instance.grid[0])):
            if (row, col) in dig_plan_instance.trench_coord:
                print('#', end=' ')
            elif (row, col) in dig_plan_instance.seen_outer_terrain:
                print('x', end=' ')
            else:
                print(dig_plan_instance.grid[row][col], end=' ')
        
        print()
    """
