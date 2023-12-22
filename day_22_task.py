# https://adventofcode.com/2023/day/22
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

class CubesDownfall:
    def __init__(self):
        self.bricks = []

    def find_supporting_positions(self, x_start, x_end, y_start, y_end, z_start, z_end, occupied_space_map):
        supporting_positions = []
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                for z in range(z_start, z_end + 1):
                    if (x, y, z - 1) in occupied_space_map:
                        supporting_positions.append((x, y, z - 1))
        return supporting_positions

    def simulate_brick_falling(self, bricks):
        total_bricks = len(bricks)
        brick_supports_map = {i: [] for i in range(total_bricks)}
        brick_supported_by_map = {i: [] for i in range(total_bricks)}
        occupied_space_map = {}

        for brick in bricks:
            (brick_end1, brick_end2, brick_id) = brick
            ((x_start, y_start, z_start), (x_end, y_end, z_end)) = brick_end1, brick_end2

            supporting_positions = []  # Initialize supporting_positions
            while z_start > 1:
                supporting_positions = self.find_supporting_positions(x_start, x_end, y_start, y_end, z_start, z_end, occupied_space_map)
                if supporting_positions:
                    break
                z_start, z_end = z_start - 1, z_end - 1

            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    for z in range(z_start, z_end + 1):
                        occupied_space_map[(x, y, z)] = brick_id

            support_ids = {occupied_space_map[pos] for pos in supporting_positions}
            for support_id in support_ids:
                brick_supports_map[support_id].append(brick_id)
                brick_supported_by_map[brick_id].append(support_id)

        return brick_supports_map, brick_supported_by_map

    def count_removable(self, brick_supports, brick_supported_by):
        removable_count = 0
        for brick_id in brick_supports:
            if all(len(brick_supported_by[support_id]) > 1 for support_id in brick_supports[brick_id]):
                removable_count += 1

        return removable_count

    def get_num_of_cubes_to_disintegrate(self, file_name):
        row = 0
        for line in FileReader().gen_file_reader(file_name):
            brick = [[int(n) for n in coord.split(",")]
                    for coord in line.split("~")]
            brick += [row]
    
            self.bricks.append(brick)
            row += 1
        self.bricks.sort(key=lambda b: b[0][2])

        brick_supports_map, brick_supported_by_map = self.simulate_brick_falling(self.bricks)
        num_of_cubes_to_disintegrate = self.count_removable(brick_supports_map, brick_supported_by_map)

        return num_of_cubes_to_disintegrate

if __name__ == '__main__':
    print('Day 22')
    cubes_downfall_instance = CubesDownfall()
    num_of_cubes_to_disintegrate = cubes_downfall_instance.get_num_of_cubes_to_disintegrate('day_22.txt')
    print('Task 1 is = ', num_of_cubes_to_disintegrate)

#389