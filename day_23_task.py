# https://adventofcode.com/2023/day/23
import sys

from collections import deque

sys.setrecursionlimit(10000)


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class SnowPath:
    def __init__(self):
        self.grid = []
        self.visited = set()
        self.starting_point = None
        self.end_point = None
        self.moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.slopes = {"^": (-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}
        self.max_steps = 0
        self.longest_path = None

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    # part 1
    def dfs_longest_path_part_1(self, start_point, end_point):
        def dfs(node, steps):
            if node == end_point:
                self.max_steps = max(self.max_steps, steps)
                return
            if node in self.visited:
                return

            self.visited.add(node)
            curr_row, curr_col = node

            # slopes
            if self.grid[curr_row][curr_col] in self.slopes:
                row_d, col_d = self.slopes[self.grid[curr_row][curr_col]]
                new_row, new_col = curr_row + row_d, curr_col + col_d
                if self.is_within_grid((new_row, new_col), self.grid) and self.grid[new_row][new_col] != "#":
                    dfs((new_row, new_col), steps + 1)

            # other moves
            else:
                for row_d, col_d in self.moves:
                    new_row, new_col = curr_row + row_d, curr_col + col_d
                    if self.is_within_grid((new_row, new_col), self.grid) and self.grid[new_row][new_col] != "#":
                        dfs((new_row, new_col), steps + 1)

            # Backtrack
            self.visited.remove(node)

        dfs(start_point, 0)
        return self.max_steps

    # part 2
    def dfs_longest_path_part_2(self, graph, steps_dict, starting_point, end_point):
        if starting_point == end_point:
            return sum(steps_dict.values())

        best_path_length = None
        for neighbor, weight in graph[starting_point].items():
            if neighbor in steps_dict:
                continue

            steps_dict[neighbor] = weight
            path_length = self.dfs_longest_path_part_2(graph, steps_dict, neighbor, end_point)

            if best_path_length is None or (path_length is not None and path_length > best_path_length):
                best_path_length = path_length

            del steps_dict[neighbor]

        return best_path_length

    def get_adj_lst(self, graph):
        adjacency_dict = {}
        for row_index, row in enumerate(graph):
            for col_index, cell in enumerate(row):
                if cell != "#":
                    adjacent_cells = {}
                    for row_delta, col_delta in self.moves:
                        neighbor_row, neighbor_col = row_index + row_delta, col_index + col_delta
                        if (
                            self.is_within_grid((neighbor_row, neighbor_col), self.grid)
                            and graph[neighbor_row][neighbor_col] != "#"
                        ):
                            adjacent_cells[(neighbor_row, neighbor_col)] = 1
                    adjacency_dict[(row_index, col_index)] = adjacent_cells

        all_keys = list(adjacency_dict.keys())
        for cell_key in all_keys:
            neighbors = adjacency_dict[cell_key]
            if len(neighbors) == 2:
                left_neighbor, right_neighbor = neighbors.keys()
                del adjacency_dict[left_neighbor][cell_key]
                del adjacency_dict[right_neighbor][cell_key]
                combined_distance = neighbors[left_neighbor] + neighbors[right_neighbor]
                adjacency_dict[left_neighbor][right_neighbor] = max(
                    adjacency_dict[left_neighbor].get(right_neighbor, 0), combined_distance
                )
                adjacency_dict[right_neighbor][left_neighbor] = max(
                    adjacency_dict[right_neighbor].get(left_neighbor, 0), combined_distance
                )
                del adjacency_dict[cell_key]

        return adjacency_dict

    def get_longest_pass(self, file_name):
        data = []
        row = 0
        for line in FileReader().gen_file_reader(file_name):
            self.grid.append(line)
            row += 1

        # detect starting point
        for index, char in enumerate(self.grid[0]):
            if char == ".":
                self.starting_point = (0, index)
                break

        # detect end point
        for index, char in enumerate(self.grid[-1]):
            if char == ".":
                self.end_point = (row - 1, index)

        # part 1
        longest_path_with_slopes = self.dfs_longest_path_part_1(self.starting_point, self.end_point)
        # part 2
        self.adj_list = self.get_adj_lst(self.grid)
        longest_path_without_slopes = self.dfs_longest_path_part_2(
            self.adj_list, {(0, 1): 0}, self.starting_point, self.end_point
        )
        return longest_path_with_slopes, longest_path_without_slopes


if __name__ == "__main__":
    print("Day 23")
    snow_path_instance = SnowPath()
    longest_path_part_1, longest_path_part_2 = snow_path_instance.get_longest_pass("day_23.txt")
    print("Task 1 is = ", longest_path_part_1)
    print("Task 2 is = ", longest_path_part_2)
