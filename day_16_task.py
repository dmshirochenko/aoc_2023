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
        self.num_of_rows = 0
        self.num_of_cols = 0
        self.moves = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}
        self.beam_reflection = {
            ("U", "/"): "R",
            ("R", "/"): "U",
            ("D", "/"): "L",
            ("L", "/"): "D",
            ("U", "\\"): "L",
            ("R", "\\"): "D",
            ("D", "\\"): "R",
            ("L", "\\"): "U",
        }

        self.beam_splitter_behavior = {
            ("U", "|"): ["U"],
            ("D", "|"): ["D"],
            ("L", "-"): ["L"],
            ("R", "-"): ["R"],
            ("U", "-"): ["L", "R"],
            ("D", "-"): ["L", "R"],
            ("L", "|"): ["U", "D"],
            ("R", "|"): ["U", "D"],
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

    def get_edge_coordinates(self, n, m):
        top_edge = [(0, i) for i in range(m)]
        right_edge = [(i, m - 1) for i in range(1, n - 1)]
        bottom_edge = [(n - 1, i) for i in range(m - 2, -1, -1)]
        left_edge = [(i, 0) for i in range(n - 2, 0, -1)]

        return top_edge, right_edge, bottom_edge, left_edge

    def bfs(self, starting_node_with_direction):
        queue = deque()
        visited_tiles = set()
        visited_states = set()

        row, col, direction = starting_node_with_direction
        queue.append(starting_node_with_direction)

        while queue:
            node_to_check = queue.popleft()
            row, col, current_directions = node_to_check
            visited_tiles.add((row, col))
            for current_direction in current_directions:
                row_d, col_d = self.moves[current_direction]
                new_row, new_col = row + row_d, col + col_d
                if (
                    self.is_within_grid((new_row, new_col), self.grid)
                    and (new_row, new_col, current_direction) not in visited_states
                ):
                    char_within_coord = self.grid[new_row][new_col]
                    if char_within_coord == ".":
                        queue.append((new_row, new_col, [current_direction]))
                        visited_states.add((new_row, new_col, current_direction))
                    else:
                        row_r, col_r, direction_r = self.get_next_direction((new_row, new_col), current_direction)
                        queue.append((row_r, col_r, direction_r))

        return len(visited_tiles)

    def get_count_of_tiles_visited_by_beam(self, file_name):
        for line in FileReader().gen_file_reader(file_name):
            self.grid.append([i for i in line])
        self.num_of_rows = len(self.grid)
        self.num_of_cols = len(self.grid[0])

        # task 1
        max_tiles_task_1 = self.bfs((0, 0, ["D"]))

        # task 2
        top_edge, right_edge, bottom_edge, left_edge = self.get_edge_coordinates(self.num_of_rows, self.num_of_cols)
        max_tiles_task_2 = max_tiles_task_1
        # top_edge
        for element in top_edge:
            row, col = element
            max_tiles_task_2 = max(max_tiles_task_2, self.bfs((row, col, ["D"])))
        # right_edge
        for element in right_edge:
            row, col = element
            max_tiles_task_2 = max(max_tiles_task_2, self.bfs((row, col, ["L"])))
        # bottom_edge
        for element in bottom_edge:
            row, col = element
            max_tiles_task_2 = max(max_tiles_task_2, self.bfs((row, col, ["U"])))
        # left_edge
        for element in left_edge:
            row, col = element
            max_tiles_task_2 = max(max_tiles_task_2, self.bfs((row, col, ["R"])))

        return max_tiles_task_1, max_tiles_task_2


if __name__ == "__main__":
    print("Day 16")
    beam_path_instance = BeamPath()
    count_of_visited_tiles_1, count_of_visited_tiles_2 = beam_path_instance.get_count_of_tiles_visited_by_beam(
        "day_16.txt"
    )
    print("Task 1 = ", count_of_visited_tiles_1)
    print("Task 2 = ", count_of_visited_tiles_2)
