# https://adventofcode.com/2023/day/3


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class SeedsMap:
    def __init__(self):
        self.seeds_ranges = []

    def initial_seed_mapper_for_task_2(self, seeds_values):
        for i in range(0, len(seeds_values), 2):
            self.seeds_ranges.append((seeds_values[i], seeds_values[i] + seeds_values[i + 1] - 1))

    def map_source_ranges(self, source_ranges, mapping_list):
        mapped_ranges = []
        for range_start, range_end in source_ranges:
            overlapping_ranges = []

            for dest_start, mapping_start, range_size in mapping_list:
                mapping_end = mapping_start + range_size - 1

                # Skip non-overlapping ranges
                if range_end < mapping_start or mapping_end < range_start:
                    continue

                # Calculate the intersection of the two ranges
                intersection_start = max(range_start, mapping_start)
                intersection_end = min(range_end, mapping_end)
                overlapping_ranges.append((intersection_start, intersection_end))

                # Adjust the range by the destination start
                adjusted_start = intersection_start - mapping_start + dest_start
                adjusted_end = intersection_end - mapping_start + dest_start
                mapped_ranges.append((adjusted_start, adjusted_end))

            # Check for uncovered sections of the range
            if not overlapping_ranges:
                mapped_ranges.append((range_start, range_end))
                continue

            overlapping_ranges.sort()

            # Check for gaps at the beginning and end of the range
            if overlapping_ranges[0][0] > range_start:
                mapped_ranges.append((range_start, overlapping_ranges[0][0] - 1))
            if overlapping_ranges[-1][1] < range_end:
                mapped_ranges.append((overlapping_ranges[-1][1] + 1, range_end))

            # Check for gaps between overlapping ranges
            for i in range(len(overlapping_ranges) - 1):
                current_end = overlapping_ranges[i][1]
                next_start = overlapping_ranges[i + 1][0]

                if next_start > current_end + 1:
                    mapped_ranges.append((current_end + 1, next_start - 1))

        return mapped_ranges

    def get_new_mapping_for_seed_task_2(self, mapping_lists):
        current_ranges = self.seeds_ranges
        for mapping in mapping_lists:
            current_ranges = self.map_source_ranges(current_ranges, mapping)
        return current_ranges

    def seeds_mapper(self, file_name):
        file_generator = FileReader().gen_file_reader("day_5.txt")
        _, values_str = next(file_generator).split(": ")
        _ = next(file_generator)  # skip next line

        seed_values = [int(value) for value in values_str.split()]
        self.initial_seed_mapper_for_task_2(seed_values)

        mapping_list = []
        current_section = []
        # parse 'map' part
        for line in file_generator:
            if "map" in line:
                if current_section:
                    mapping_list.append(current_section)
                    current_section = []
                section_name = line.split(":")[0]
            elif line:
                current_section.append([int(num) for num in line.split()])
        else:
            mapping_list.append(current_section)

        location_mapping = self.get_new_mapping_for_seed_task_2(mapping_list)
        return location_mapping


if __name__ == "__main__":
    print("Day 5")
    seeds_map_instance = SeedsMap()
    location_mapping = seeds_map_instance.seeds_mapper("day_5.txt")
    min_location = float("inf")
    print("Task 2 = ", min(location_mapping)[0])
