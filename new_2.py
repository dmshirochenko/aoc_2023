from functools import lru_cache
from typing import Tuple

def parse_input_file(filename: str):
    """
    Reads the input file and parses each line into a tuple of string and another tuple of integers.
    """
    parsed_data = []
    for line in open(filename).readlines():
        pixel_pattern, group_sizes_str = line.split(" ")
        group_sizes = tuple(map(int, group_sizes_str.split(",")))
        parsed_data.append((pixel_pattern, group_sizes))
    return parsed_data

@lru_cache(maxsize=None)
def arrangement_count(pixel_pattern: str, group_sizes: Tuple[int], is_next_lava: bool) -> int:
    """
    Counts the number of valid arrangements for a given pixel pattern and group sizes.
    m = pixel pattern ("#?.#"), s = group sizes (1,2,3), n = is next spot lava
    """
    # Helper function to transform the group sizes tuple
    transform_group_sizes = lambda sizes: (sizes[0] - 1,) + sizes[1:]

    if not group_sizes:
        return 0 if "#" in pixel_pattern else 1
    elif not pixel_pattern:
        return 0 if sum(group_sizes) else 1
    elif group_sizes[0] == 0:
        return arrangement_count(pixel_pattern[1:], group_sizes[1:], False) if pixel_pattern[0] in ["?", "."] else 0
    elif is_next_lava:
        return arrangement_count(pixel_pattern[1:], transform_group_sizes(group_sizes), True) if pixel_pattern[0] in ["?", "#"] else 0
    elif pixel_pattern[0] == "#":
        return arrangement_count(pixel_pattern[1:], transform_group_sizes(group_sizes), True)
    elif pixel_pattern[0] == ".":
        return arrangement_count(pixel_pattern[1:], group_sizes, False)
    else:
        return arrangement_count(pixel_pattern[1:], group_sizes, False) + arrangement_count(pixel_pattern[1:], transform_group_sizes(group_sizes), True)

# Parse the input file
input_data = parse_input_file("day_12.txt")

# Calculate and print the total count of arrangements for the original data
print(sum(arrangement_count(pixel_pattern, group_sizes, False) for pixel_pattern, group_sizes in input_data))

"""
# Create modified data by repeating each pattern and group sizes
modified_data = [(((pixel_pattern + "?") * 5)[:-1], group_sizes * 5) for pixel_pattern, group_sizes in input_data]

# Calculate and print the total count of arrangements for the modified data
print(sum(arrangement_count(pixel_pattern, group_sizes, False) for pixel_pattern, group_sizes in modified_data))
"""