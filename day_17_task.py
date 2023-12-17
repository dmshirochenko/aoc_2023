# https://adventofcode.com/2023/day/17
import heapq


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class CruciblesWheels:
    def __init__(self):
        self.grid = []
        self.moves = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}
        self.opposite_moves = {"U": "D", "D": "U", "R": "L", "L": "R"}

    def is_within_grid(self, coordinates, grid):
        x, y = coordinates
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def get_possible_directions_old(self, current_direction, same_direction_counter):
        set_of_possible_directions = {key for key in self.moves.keys()}

        if current_direction is not None:
            set_of_possible_directions.remove(self.opposite_moves[current_direction])
        if same_direction_counter == 3:
            set_of_possible_directions.remove(current_direction)

        return set_of_possible_directions

    def get_possible_directions(self, current_direction, same_direction_counter, case_num):
        set_of_possible_directions = {key for key in self.moves.keys()}

        if current_direction is not None:
            set_of_possible_directions.remove(self.opposite_moves[current_direction])

        if case_num == 1:
            if same_direction_counter == 3:
                set_of_possible_directions.remove(current_direction)

        elif case_num == 2:
            if same_direction_counter and same_direction_counter < 4:
                set_of_possible_directions = {current_direction}
            elif same_direction_counter == 10:
                set_of_possible_directions.remove(current_direction)

        return set_of_possible_directions

    def dijkstra(self, starting_point, end_point, case_num):
        _, _, coord_starting_point, _, _, _ = starting_point
        _, _, coord_end_point, _, _, _ = end_point
        heap = []
        seen_blocks = set()

        heapq.heappush(heap, (0, 2, (0, 0), None, None))
        while heap:
            check_node = heapq.heappop(heap)
            sum_of_heat_node, val, coord, direction, same_direction_counter = check_node
            node_to_check = (coord, direction, same_direction_counter)

            if coord == coord_end_point:
                return sum_of_heat_node

            if node_to_check not in seen_blocks:
                seen_blocks.add(node_to_check)

                set_of_possible_directions = self.get_possible_directions(
                    direction, same_direction_counter, case_num=case_num
                )
                for move_key, move_value in self.moves.items():
                    if move_key in set_of_possible_directions:
                        row_c, col_c = coord
                        row_d, col_d = move_value
                        row_new, col_new = row_c + row_d, col_c + col_d
                        if self.is_within_grid((row_new, col_new), self.grid):
                            sum_of_heat_node_new = sum_of_heat_node + self.grid[row_new][col_new][1]
                            val_new = self.grid[row_new][col_new][1]
                            coord_new = (row_new, col_new)
                            direction_new = move_key

                            if move_key == direction:
                                if same_direction_counter is None:
                                    same_direction_counter_new = 1
                                else:
                                    same_direction_counter_new = same_direction_counter + 1
                            else:
                                same_direction_counter_new = 1

                            block_to_push = (
                                sum_of_heat_node_new,
                                val_new,
                                coord_new,
                                direction_new,
                                same_direction_counter_new,
                            )
                            heapq.heappush(heap, block_to_push)

        return -1

    def get_sum_of_less_heated_route(self, file_name, case_num):
        row = 0
        self.grid = []
        for line in FileReader().gen_file_reader(file_name):
            row_to_add = [(float("inf"), int(line[col]), (row, col), None, None, None) for col in range(len(line))]
            self.grid.append(row_to_add)
            row += 1

        sum_of_less_heated_route = self.dijkstra(self.grid[0][0], self.grid[-1][-1], case_num=case_num)
        return sum_of_less_heated_route


if __name__ == "__main__":
    print("Day 17")
    crucibles_wheels_instance = CruciblesWheels()
    sum_of_less_heated_route_task_1 = crucibles_wheels_instance.get_sum_of_less_heated_route(
        file_name="day_17.txt", case_num=1
    )
    print("Task 1 = ", sum_of_less_heated_route_task_1)
    sum_of_less_heated_route_task_2 = crucibles_wheels_instance.get_sum_of_less_heated_route(
        file_name="day_17.txt", case_num=2
    )
    print("Task 2 = ", sum_of_less_heated_route_task_2)
