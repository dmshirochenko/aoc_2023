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
        self.grid = []
        self.expanded_grid = None
        self.pipe_map = {
            "|": {"N": ["|", "7", "F"], "E": [], "S": ["|", "L", "J"], "W": []},
            "-": {"N": [], "E": ["-", "J", "7"], "S": [], "W": ["-", "L", "F"]},
            "L": {"N": ["|", "7", "F"], "E": ["-", "J", "7"], "S": [], "W": []},
            "J": {"N": ["|", "7", "F"], "E": [], "S": [], "W": ["-", "L", "F"]},
            "7": {"N": [], "E": [], "S": ["|", "L", "J"], "W": ["-", "L", "F"]},
            "F": {"N": [], "E": ["-", "J", "7"], "S": ["|", "L", "J"], "W": []},
            "S": {"E": ["-"], "S": [], "N": [], "W": ["F"]},  # changed for each case (fair for my input)
        }
        self.pipe_to_rebuild_map = {
            "|": ["N", "S"],
            "-": ["E", "W"],
            "L": ["N", "E"],
            "J": ["N", "W"],
            "7": ["S", "W"],
            "F": ["S", "E"],
        }
        self.moves = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
        self.path = None
        self.seen_outer_loop_tiles = set()

    def finish_extended_pipe(self):
        set_of_borders = set()
        for row, col in self.doubled_path:
            pipe_type = self.expanded_grid[row][col]
            if pipe_type == "S":
                continue
            for move_to_do in self.pipe_to_rebuild_map[pipe_type]:
                row_diff, col_diff = self.moves[move_to_do]
                new_row, new_col = row + row_diff, col + col_diff
                if self.is_within_grid((new_row, new_col), self.expanded_grid):
                    self.expanded_grid[new_row][new_col] = "X"
                    set_of_borders.add((new_row, new_col))

        self.doubled_path.update(set_of_borders)

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def is_possible_to_connect(self, curr_pipe, new_pipe, direction):
        is_possible = False
        for possbile_pipes in self.pipe_map[curr_pipe][direction]:
            for pipe in possbile_pipes:
                if pipe == new_pipe:
                    is_possible = True

        return is_possible

    def expand_grid(self, original_grid):
        expanded_grid = []
        for original_row in original_grid:
            expanded_row = []
            for cell_value in original_row:
                expanded_row.extend([cell_value, "*"])
            expanded_grid.append(expanded_row)
            expanded_grid.append(["*" for _ in expanded_row])
        return expanded_grid

    def double_coords(self, coords):
        return {(int(2 * cx), int(2 * cy)) for cx, cy in coords}

    def bfs_to_find_outer_loop(self, grid, starting_point):
        if starting_point not in self.doubled_path:
            queue = deque([starting_point])
            self.seen_outer_loop_tiles.add(starting_point)

            while queue:
                node = queue.popleft()
                curr_row, curr_col = node
                for direction, coor_diff in self.moves.items():
                    row_diff, col_diff = coor_diff
                    new_row, new_col = curr_row + row_diff, curr_col + col_diff
                    if self.is_within_grid((new_row, new_col), self.expanded_grid):
                        if (new_row, new_col) not in self.seen_outer_loop_tiles and (
                            new_row,
                            new_col,
                        ) not in self.doubled_path:
                            self.seen_outer_loop_tiles.add((new_row, new_col))
                            queue.append((new_row, new_col))

    def bfs_to_find_loop_path(self):
        queue = deque([self.starting_point])
        seen = {self.starting_point}
        num_of_steps = -1

        while queue:
            queue_len = len(queue)
            for _ in range(queue_len):
                node = queue.popleft()
                curr_row, curr_col = node
                curr_pipe_key = self.grid[curr_row][curr_col]
                for direction, coor_diff in self.moves.items():
                    row_diff, col_diff = coor_diff
                    new_row, new_col = curr_row + row_diff, curr_col + col_diff
                    if self.is_within_grid((new_row, new_col), self.grid):
                        new_pipe_key = self.grid[new_row][new_col]
                        if self.is_possible_to_connect(curr_pipe_key, new_pipe_key, direction):
                            if (new_row, new_col) not in seen:
                                seen.add((new_row, new_col))
                                queue.append((new_row, new_col))

            num_of_steps += 1
        self.path = seen
        return num_of_steps

    def get_steps_to_farthest_point(self, file_name):
        temp_list = []
        row = 0
        for line in FileReader().gen_file_reader(file_name):
            for col, char in enumerate(line):
                if char == "S":
                    self.starting_point = (row, col)
                temp_list.append(char)
            self.grid.append(temp_list)
            temp_list = []
            row += 1

        # task 1
        num_of_steps = self.bfs_to_find_loop_path()  # result will be stored in self.path

        # task 2
        self.expanded_grid = pipes_instance.expand_grid(self.grid)
        self.doubled_path = pipes_instance.double_coords(pipes_instance.path)
        self.finish_extended_pipe()
        self.bfs_to_find_outer_loop(self.expanded_grid, (0, 0))

        return num_of_steps


if __name__ == "__main__":
    print("Day 10")
    pipes_instance = Pipes()
    num_of_steps = pipes_instance.get_steps_to_farthest_point("day_10.txt")
    # task 1
    print("Task 1 = ", num_of_steps)
    # task 2 count all inner symbols except "*" which we used for extention
    count = 0
    for row in range(len(pipes_instance.expanded_grid)):
        for col in range(len(pipes_instance.expanded_grid[0])):
            if ((row, col) not in pipes_instance.doubled_path) and (
                (row, col) not in pipes_instance.seen_outer_loop_tiles
            ):
                tiles_type = pipes_instance.expanded_grid[row][col]
                if tiles_type != "*":
                    count += 1

    print("Task 2 = ", count)

    # HTML vizualization
    with open("output_day_10.html", "w") as file:
        file.write("<html><body><pre>")  # Start of HTML file
        for row in range(len(pipes_instance.expanded_grid)):
            for col in range(len(pipes_instance.expanded_grid[row])):
                if (row, col) in pipes_instance.doubled_path:
                    file.write(
                        f'<span style="background-color: green;">{pipes_instance.expanded_grid[row][col]}</span> '
                    )
                elif (row, col) in pipes_instance.seen_outer_loop_tiles:
                    file.write(f'<span style="background-color: red;">{pipes_instance.expanded_grid[row][col]}</span> ')
                else:
                    file.write(str(pipes_instance.expanded_grid[row][col]) + " ")
            file.write("<br>")  # New line in HTML
        file.write("</pre></body></html>")  # End of HTML file
