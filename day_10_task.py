# https://adventofcode.com/2023/day/10
from collections import deque

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class Pipes:
    def __init__(self):
        self.starting_point = None
        self.grid_size = None
        self.pipe_map = {
            '|': {'N': ['|', '7', 'F'], 'E': [], 'S': ['|', 'L', 'J'], 'W': []},
            '-': {'N': [], 'E': ['-', 'J', '7'], 'S': [], 'W': ['-', 'L', 'F']},
            'L': {'N': ['|', '7', 'F'], 'E': ['-', 'J', '7'], 'S': [], 'W': []},
            'J': {'N': ['|', '7', 'F'], 'E': [], 'S': [], 'W': ['-', 'L', 'F']},
            '7': {'N': [], 'E': [], 'S': ['|', 'L', 'J'], 'W': ['-', 'L', 'F']},
            'F': {'N': [], 'E': ['-', 'J', '7'], 'S': ['|', 'L', 'J'], 'W': []},
            'S': {'E': ['-'], 'S': [], 'N': [], 'W': ['F']} #changed for each case 
        }
        self.moves = {
            'N': (-1, 0),
            'E': (0, 1),
            'S': (1, 0),
            'W': (0, -1)
        }

    def is_within_grid(self, coordinates):
        x, y = coordinates
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]

    def is_possible_to_connect(self, curr_pipe, new_pipe, direction):
        is_possible = False
        for possbile_pipes in self.pipe_map[curr_pipe][direction]:
            for pipe in possbile_pipes:
                if pipe == new_pipe:
                    is_possible = True

        return is_possible

    def bfs_to_follow_animal(self, grid):
        queue = deque([self.starting_point])
        seen = {self.starting_point}
        num_of_steps = -1

        while queue:
            queue_len = len(queue)
            for _ in range(queue_len):
                node = queue.popleft()
                curr_row, curr_col = node
                curr_pipe_key = grid[curr_row][curr_col]
                for direction, coor_diff in self.moves.items():
                    row_diff, col_diff = coor_diff
                    new_row, new_col = curr_row + row_diff, curr_col + col_diff
                    if self.is_within_grid((new_row, new_col)):
                        new_pipe_key = grid[new_row][new_col]
                        if self.is_possible_to_connect(curr_pipe_key, new_pipe_key, direction):
                            if (new_row, new_col) not in seen:
                                seen.add((new_row, new_col))
                                queue.append((new_row, new_col))
            
            num_of_steps += 1
                    
        return num_of_steps

    def get_steps_to_farthest_point(self, file_name):
        grid = []
        temp_list = []
        row = 0
        for line in FileReader().gen_file_reader(file_name):
            for col, char in enumerate(line):
                if char == 'S':
                    self.starting_point = (row, col)
                temp_list.append(char)
            grid.append(temp_list)
            temp_list = []
            row += 1
        
        self.grid_size = (len(grid), len(grid[0]))
        num_of_steps = self.bfs_to_follow_animal(grid)

        return num_of_steps

if __name__ == '__main__':
    print('Day 10')
    pipes_instance = Pipes()
    num_of_steps = pipes_instance.get_steps_to_farthest_point('day_10.txt')
    print('Task 1 = ', num_of_steps)