# https://adventofcode.com/2023/day/23
import itertools


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class HailCollider:
    def __init__(self):
        self.x_frame_min = 200000000000000
        self.x_frame_max = 400000000000000
        self.y_frame_min = 200000000000000
        self.y_frame_max = 400000000000000

    def find_intersection(self, point1_line1, point2_line1, point1_line2, point2_line2):
        def calculate_slope(point1, point2):
            (x1, y1), (x2, y2) = point1, point2
            if x2 - x1 == 0:
                return float("inf")
            return (y2 - y1) / (x2 - x1)

        m1 = calculate_slope(point1_line1, point2_line1)
        m2 = calculate_slope(point1_line2, point2_line2)

        (x1, y1), (_, _) = point1_line1, point2_line1
        (x3, y3), (_, _) = point1_line2, point2_line2

        if m1 == m2:
            if y1 == m1 * x1 + ((y3 - m2 * x3) - m2 * x1):
                print("The lines are coincident")
                return False
            else:
                print("The lines are parallel and do not intersect")
                return False

        x = ((y3 - m2 * x3) - (y1 - m1 * x1)) / (m1 - m2)
        y = m1 * x + (y1 - m1 * x1)

        return x, y

    def cal_next_point_of_the_line(self, point_tuple):
        coord, velocity = point_tuple
        x, y, z = coord
        velocity_x, velocity_y, velocity_z = velocity
        coord_x_new, coord_y_new, coord_z_new = x + velocity_x, y + velocity_y, z + velocity_z

        return (coord_x_new, coord_y_new)

    def is_it_in_frame(self, point1_line1, line_vel_1, point1_line2, line_vel_2, point_coord_intersection):
        if not self.is_point_in_frame(point_coord_intersection):
            return False

        return self.is_point_in_future(point1_line1, line_vel_1, point_coord_intersection) and self.is_point_in_future(
            point1_line2, line_vel_2, point_coord_intersection
        )

    def is_point_in_frame(self, point):
        x, y = point
        return (self.x_frame_min <= x <= self.x_frame_max) and (self.y_frame_min <= y <= self.y_frame_max)

    def is_point_in_future(self, start_point, velocity, intersection_point):
        rel_pos_x = intersection_point[0] - start_point[0]
        rel_pos_y = intersection_point[1] - start_point[1]

        return (velocity[0] * rel_pos_x >= 0) and (velocity[1] * rel_pos_y >= 0)

    def get_num_of_crosses(self, file_name):
        data = []
        for line in FileReader().gen_file_reader(file_name):
            coord_str, velocity_str = line.split(" @ ")
            coord = tuple([int(i) for i in coord_str.split(",")])
            velocity = tuple([int(i) for i in velocity_str.split(",")])
            tuple_of_coord_velocity = (coord, velocity)
            data.append(tuple_of_coord_velocity)

        unique_pairs = [(data[i], data[j]) for i in range(len(data)) for j in range(i + 1, len(data))]

        count_intersections = 0
        for pair in unique_pairs:
            point_1_tuple, point_2_tuple = pair
            point_1_x, point_1_y, _ = point_1_tuple[0]
            point_2_x, point_2_y, _ = point_2_tuple[0]
            # first points
            point1_line1 = (point_1_x, point_1_y)
            point1_line2 = (point_2_x, point_2_y)
            # second points
            point2_line1 = self.cal_next_point_of_the_line(point_1_tuple)
            point2_line2 = self.cal_next_point_of_the_line(point_2_tuple)
            point_coord_intersection = self.find_intersection(point1_line1, point2_line1, point1_line2, point2_line2)
            if point_coord_intersection:
                line_vel_1_x, line_vel_1_y, _ = point_1_tuple[1]
                line_vel_2_x, line_vel_2_y, _ = point_2_tuple[1]
                line_vel_1 = line_vel_1_x, line_vel_1_y
                line_vel_2 = line_vel_2_x, line_vel_2_y
                if self.is_it_in_frame(point1_line1, line_vel_1, point1_line2, line_vel_2, point_coord_intersection):
                    count_intersections += 1

        return count_intersections


if __name__ == "__main__":
    print("Day 24")
    hail_collider_instance = HailCollider()
    num_of_crosses = hail_collider_instance.get_num_of_crosses("day_24.txt")
    print("Task 1 is = ", num_of_crosses)
