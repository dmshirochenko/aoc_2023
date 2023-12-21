# https://adventofcode.com/2023/day/20
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


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

    def bfs(self, start, max_dist):
        queue = deque()
        row_start, col_start, step = start

        parity = max_dist % 2
        print(parity)
        queue.append(start)

        num_tiles = 0
        while queue:
            curr_row, curr_col, step = queue.popleft()
            if step > max_dist:
                break
            if (curr_row, curr_col) in self.seen_tiles:
                continue
            self.seen_tiles.add((curr_row, curr_col))

            if step % 2 == parity:
                num_tiles += 1

            for move in self.moves:
                row_d, col_d = move
                row_new, col_new = curr_row + row_d, curr_col + col_d
                if self.is_within_grid((row_new, col_new), self.grid):
                    if self.grid[row_new][col_new] != "#":
                        queue.append((row_new, col_new, step + 1))

        return num_tiles

    def get_num_of_tiles_elf_can_visit(self, file_name):
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
        num_of_visited_tiles_part_1 = self.bfs((row_start, col_start, step), max_dist)
        return num_of_visited_tiles_part_1


if __name__ == "__main__":
    print("Day 21")
    elf_journey_instance = ElfJourney()
    # part 1
    max_dist = 64
    num_of_tiles_visited = elf_journey_instance.get_num_of_tiles_elf_can_visit("day_21.txt", max_dist)
    print("Task 1 is = ", num_of_tiles_visited)

    """
    for row in range(len(elf_journey_instance.grid)):
        for col in range(len(elf_journey_instance.grid[0])):
            if (row, col) in elf_journey_instance.seen_tiles:
                print("O", end=' ')
            else:
                print(elf_journey_instance.grid[row][col], end=' ')
        
        print()
    
    """
