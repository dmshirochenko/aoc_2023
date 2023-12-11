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
        queue = deque([starting_node])
        seen_nodes = {starting_node}
        num_of_laps = 0
        if self.set_of_galaxies:
            while queue:
                len_of_queue = len(queue)
                for _ in range(len_of_queue):
                    node = queue.popleft()
                    row_curr, col_curr = node
                    if (node in self.set_of_galaxies) and (node not in self.explored_nodes):
                        if (row_curr, col_curr) in self.shortest_path:
                            self.shortest_path[starting_node].append(((node), num_of_laps))
                        else:
                            self.shortest_path[starting_node] = ((node), num_of_laps)
                    for move in self.moves:
                        row_d, col_d = move
                        new_row = row_curr + row_d
                        new_col = col_curr + col_d
                        if self.is_within_grid((new_row, new_col), self.galaxy_grid):
                            if (new_row, new_col) not in seen_nodes:
                                seen_nodes.add((new_row, new_col))
                                queue.append((new_row, new_col))


                num_of_laps += 1

    def add_dot_to_columns(self):
        num_rows = len(self.galaxy_grid)
        num_cols = len(self.galaxy_grid[0]) if self.galaxy_grid else 0

        new_cols_to_add = [False] * num_cols

        for col in range(num_cols):
            if all(self.galaxy_grid[row][col] == '.' for row in range(num_rows)):
                new_cols_to_add[col] = True

        for col in range(num_cols - 1, -1, -1):
            if new_cols_to_add[col]:
                for row in range(num_rows):
                    self.galaxy_grid[row].insert(col + 1, '.')

    def display(self):
        for row in self.galaxy_grid:
            print(' '.join(row))

    def get_sum_of_shortest_path(self, file_name):
        sum_of_shortest_path = 0
        row_num = 0
        #read + line expansion
        for line in FileReader().gen_file_reader(file_name):
            line_without_galaxies = True
            temp_lst = []
            for col_num, char in enumerate(line):
                if char == '#':
                    line_without_galaxies = False
                temp_lst.append(char)
            if line_without_galaxies:
                for _ in range(2):
                    self.galaxy_grid.append(temp_lst)
            else:
                self.galaxy_grid.append(temp_lst)

            row_num += 1

        self.add_dot_to_columns()

        for row_num, row in enumerate(self.galaxy_grid):
            for col_num, value in enumerate(row):
                if value == '#':
                    line_without_galaxies = False
                    self.set_of_galaxies.add((row_num, col_num))
                    self.shortest_path[(row_num, col_num)] = []


        for node in self.set_of_galaxies:
            self.explored_nodes.add(node)
            self.bfs_shortest_path(node)

        #print(self.shortest_path)
        for lst in self.shortest_path.values():
            for node, path_len in lst:
                sum_of_shortest_path += path_len


        return sum_of_shortest_path


if __name__ == '__main__':
    print('Day 11')
    galaxy_explorer_instance = GalaxyExplorer()
    sum_of_shortest_path = galaxy_explorer_instance.get_sum_of_shortest_path('day_11.txt')
    print('Task 1 = ', sum_of_shortest_path)