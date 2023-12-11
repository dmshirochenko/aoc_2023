# https://adventofcode.com/2023/day/11
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class GalaxyExplorer:
    def __init__(self):
        self.galaxy_grid = []
        self.set_of_galaxies = set()
        self.explored_nodes = set()
        self.shortest_path = {}
        self.moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def bfs_shortest_path(self, starting_node):
        queue = deque([(starting_node, (0, 0))])
        seen_nodes = {starting_node}
        num_of_laps = 0
        while queue:
            node, depth = queue.popleft()
            depth_task_1, depth_task_2 = depth
            row_curr, col_curr = node
            if self.galaxy_grid[row_curr][col_curr] == "$":
                depth_task_1 += 2 - 1
                depth_task_2 += 1000000 - 1
            if (node in self.set_of_galaxies) and (node not in self.explored_nodes):
                if (row_curr, col_curr) in self.shortest_path:
                    self.shortest_path[starting_node].append(((node), (depth_task_1, depth_task_2)))
                else:
                    self.shortest_path[starting_node] = ((node), (depth_task_1, depth_task_2))
            for move in self.moves:
                row_d, col_d = move
                new_row = row_curr + row_d
                new_col = col_curr + col_d
                if self.is_within_grid((new_row, new_col), self.galaxy_grid):
                    if (new_row, new_col) not in seen_nodes:
                        seen_nodes.add((new_row, new_col))
                        queue.append(((new_row, new_col), (depth_task_1 + 1, depth_task_2 + 1)))

    def replace_dots_in_columns(self):
        num_rows = len(self.galaxy_grid)
        num_cols = len(self.galaxy_grid[0])
        dot_columns = set()
        for col in range(num_cols):  # find cols with all '.'
            if all(self.galaxy_grid[row][col] == "." for row in range(num_rows)):
                dot_columns.add(col)
        for col in dot_columns:  # replace cols with all '.' to '$'
            for row in range(num_rows):
                self.galaxy_grid[row][col] = "$"

    def replace_dots_in_specified_rows(self, dot_rows):
        num_cols = len(self.galaxy_grid[0])

        for row in dot_rows:  # replace rows with all '.' to '$'
            for col in range(num_cols):
                if self.galaxy_grid[row][col] == ".":
                    self.galaxy_grid[row][col] = "$"

    def display(self):
        for row in self.galaxy_grid:
            print(" ".join(row))

    def get_sum_of_shortest_path(self, file_name):
        row_num = 0
        dot_rows = set()
        for line in FileReader().gen_file_reader(file_name):
            line_without_galaxies = True
            temp_lst = []
            for col_num, char in enumerate(line):
                if char == "#":
                    line_without_galaxies = False
                    self.set_of_galaxies.add((row_num, col_num))
                    self.shortest_path[(row_num, col_num)] = []
                temp_lst.append(char)
            if line_without_galaxies:
                dot_rows.add(row_num)

            self.galaxy_grid.append(temp_lst)

            row_num += 1

        self.replace_dots_in_columns()  # made a replacement for all '.' cols
        self.replace_dots_in_specified_rows(dot_rows)  # made a replacement for all '.' rows

        # do bfs for find short pass
        for node in self.set_of_galaxies:
            self.explored_nodes.add(node)
            self.bfs_shortest_path(node)

        sum_of_shortest_path_task_1 = sum_of_shortest_path_task_2 = 0
        # calculate shortest path sum
        for lst in self.shortest_path.values():
            for node, path_len in lst:
                path_len_task_1, path_len_task_2 = path_len
                sum_of_shortest_path_task_1 += path_len_task_1
                sum_of_shortest_path_task_2 += path_len_task_2

        return sum_of_shortest_path_task_1, sum_of_shortest_path_task_2


if __name__ == "__main__":
    print("Day 11")
    galaxy_explorer_instance = GalaxyExplorer()
    sum_of_shortest_path_task_1, sum_of_shortest_path_task_2 = galaxy_explorer_instance.get_sum_of_shortest_path(
        "day_11.txt"
    )
    print("Task 1 = ", sum_of_shortest_path_task_1)
    print("Task 2 = ", sum_of_shortest_path_task_2)
