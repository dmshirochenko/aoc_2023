# https://adventofcode.com/2023/day/16
from collections import deque

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

class BeamPath:
    def __init__(self):
        self.grid = []
        self.visited_tiles = set()
        self.visited_states = set()
        self.moves = {
            "U": (-1, 0),
            "L": (0, -1),
            "D": (1, 0),
            "R": (0, 1)
        }
        self.beam_reflection = {
            ("U", "/"): "R",
            ("U", "\\"): "L",
            ("R", "/"): "U",
            ("R", "\\"): "D",
            ("D", "/"): "L",
            ("D", "\\"): "R",
            ("L", "/"): "D",
            ("L", "\\"): "U"
        }

        self.beam_splitter_behavior = {
            # Pointy end encounters
            ("U", "|"): ["U"], 
            ("D", "|"): ["D"], 
            ("L", "-"): ["L"], 
            ("R", "-"): ["R"],
            # Flat side encounters
            ("U", "-"): ["L", "R"], 
            ("D", "-"): ["L", "R"],
            ("L", "|"): ["U", "D"], 
            ("R", "|"): ["U", "D"]
        }

 

    def get_next_direction(self, coordinates, current_direction):
        row, col = coordinates
        char_in_grid = self.grid[row][col]

        if char_in_grid in ("/", "\\"):
            new_direction = self.beam_reflection[(current_direction, char_in_grid)]
            next_directions = (row, col, [new_direction])
        elif char_in_grid in ("|", "-"):
            new_directions = self.beam_splitter_behavior[(current_direction, char_in_grid)]
            next_directions = (row, col, new_directions)
        return next_directions
    
    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])


    def bfs(self, starting_node_with_direction):
        row, col, direction = starting_node_with_direction
        queue = deque()
        
        queue.append(starting_node_with_direction)

        while queue:
            node_to_check = queue.popleft()
            row, col, current_directions = node_to_check
            self.visited_tiles.add((row, col))
            for current_direction in current_directions:              
                row_d, col_d = self.moves[current_direction]
                new_row, new_col = row + row_d, col + col_d
                if self.is_within_grid((new_row, new_col), self.grid) and (new_row, new_col, current_direction) not in self.visited_states:
                    char_within_coord = self.grid[new_row][new_col]
                    if char_within_coord == '.':
                        queue.append((new_row, new_col, [current_direction]))
                        self.visited_states.add((new_row, new_col, current_direction))
                    else:
                        row_r, col_r, direction_r = self.get_next_direction((new_row, new_col), current_direction)
                        queue.append((row_r, col_r, direction_r))


    def get_count_of_tiles_visited_by_beam(self, file_name):
        max_tiles
        for line in FileReader().gen_file_reader(file_name):
            self.grid.append([i for i in line])

        max_tiles = self.bfs((0, 0, ['D']))

        
        return len(self.visited_tiles)

if __name__ == '__main__':
    print('Day 16')
    beam_path_instance = BeamPath()
    count_of_visited_tiles = beam_path_instance.get_count_of_tiles_visited_by_beam('day_16.txt')
    print('Task 1 = ', count_of_visited_tiles)
    

    """
    for row in range(len(beam_path_instance.grid)):
        for col in range(len(beam_path_instance.grid[0])):
            if (row, col) in beam_path_instance.visited_tiles:
               beam_path_instance.grid[row][col] = '#' 
        
        print(beam_path_instance.grid[row])
    """ 