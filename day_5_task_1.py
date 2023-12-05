# https://adventofcode.com/2023/day/3


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

class SeedsMap():
    def __init__(self):
        self.seeds_map = dict()

    def initial_seed_mapper(self, seeds_values):
        for seed in seeds_values:
            self.seeds_map[seed] = []

    def value_mapper(self, value, mapping_list):
        new_value = value
        for range_lst in mapping_list:
            dest_range_start, source_range_start, range_len = range_lst
            if source_range_start <= value < source_range_start + range_len:
                new_value = value - (source_range_start-dest_range_start)

        return new_value

    def get_new_mapping_for_seed(self, mapping_list, is_first_mapping_session):
        if is_first_mapping_session:
            for key in self.seeds_map:
                temp_dict = dict()
                temp_dict[key] = self.value_mapper(key, mapping_list)
                for key in temp_dict.keys():
                    self.seeds_map[key].append(temp_dict[key])
        else:
            for seed, value in self.seeds_map.items():
                value_to_check = value[-1]
                temp_dict = dict()
                temp_dict[value_to_check] = self.value_mapper(value_to_check, mapping_list)
                for key in temp_dict.keys():
                    self.seeds_map[seed].append(temp_dict[key])

    def seeds_mapper(self, file_name):
        file_generator = FileReader().gen_file_reader("day_5.txt")
        _, values_str = next(file_generator).split(': ')
        _ = next(file_generator) # skip next line

        seed_values = [int(value) for value in values_str.split()]
        self.initial_seed_mapper(seed_values)
        
        current_section = []
        is_first_mapping_session = True
        #parse 'map' part
        for line in file_generator:
            if "map" in line:
                if current_section:
                    self.get_new_mapping_for_seed(current_section, is_first_mapping_session)
                    is_first_mapping_session = False
                    current_section = []
                section_name = line.split(':')[0]
            elif line:
                current_section.append([int(num) for num in line.split()])
        
        # final 'map' section
        if current_section:
            self.get_new_mapping_for_seed(current_section, is_first_mapping_session)
        
        
if __name__ == "__main__":
    print("Day 5")
    seeds_map_instance = SeedsMap()
    seeds_map_instance.seeds_mapper('day_5.txt')
    min_location = float('inf')
    #print(seeds_map_instance.seeds_map)
    for value in seeds_map_instance.seeds_map.values():
        min_location = min(min_location, value[-1])

    print('Task 1 = ', min_location)