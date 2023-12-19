# https://adventofcode.com/2023/day/19
import re
import math
import operator
from itertools import combinations
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class PartsSorter:
    def __init__(self):
        self.workflows_dct = {}
        self.workflow_adj_lst = {}
        self.string_to_sign = {
                '<': operator.lt,
                '>': operator.gt,
                '==': operator.eq,
                '<=': operator.le,
                '>=': operator.ge,
                '!=': operator.ne
            }
        self.parts_patern = r'([a-zA-Z])=(\d+)'
        self.workflow_pattern = r'([a-zA-Z])([<>=!]+)(\d+)(:[a-zA-Z]+)?'

    #task 2
    def negate_condition(self, condition):
        variable, operator, value = condition
        if operator == '>':
            negated_operator = '<='
        else:
            negated_operator = '>='

        return (variable, negated_operator, value)

    def get_workflow_adj_list(self):
        for key_rule, value in self.workflows_dct.items():
            self.workflow_adj_lst[key_rule] = {}
            splitter_rule = value.split(',')
            for rule in splitter_rule:
                get_match = re.search(self.workflow_pattern, rule)
                if get_match:
                    key, operator, value, unit = get_match.groups()
                    value = int(value)
                    unit = unit.strip(':') if unit else None
                    self.workflow_adj_lst[key_rule][(key, operator, value)] = unit
                else:
                    self.workflow_adj_lst[key_rule][None] = rule

    def bfs_to_find_possible_accepted_conditions(self):
        accepted_conditions = []
        queue = deque()
        queue.append(('in', []))

        while queue:
            current_rule, accumulated_conditions = queue.popleft()

            if current_rule.endswith('A'):
                accepted_conditions.append((current_rule, accumulated_conditions))
                continue
            elif current_rule.endswith('R'):
                continue

            last_rule = current_rule.split()[-1]
            for condition, next_rule_suffix in self.workflow_adj_lst[last_rule].items():
                next_rule = f"{current_rule} {next_rule_suffix}"
                new_conditions = accumulated_conditions.copy()

                if condition is not None:
                    new_conditions.append(condition)
                    accumulated_conditions.append(self.negate_condition(condition))

                queue.append((next_rule, new_conditions))

        return accepted_conditions
    
    #task 1
    def workflow_parser(self, rule, part):
        workflow_result = None
        splitter_rule = rule.split(',')
        for rule in splitter_rule:
            get_match = re.search(self.workflow_pattern, rule)
            if get_match:
                key, operator, value, unit = get_match.groups()
                value = int(value)
                unit = unit.strip(':') if unit else None
                if self.string_to_sign[operator](part[key], value):           
                    workflow_result = unit
                    break
            else:
                workflow_result = rule

        return workflow_result

    def parts_workflow(self, part):
        curr_rule = 'in'
        while True:
            if curr_rule == 'A' or curr_rule == 'R':
                return curr_rule
            else:
                curr_rule = self.workflow_parser(self.workflows_dct[curr_rule], part)

    def generate_combinations(self):
        for combination in combinations(range(1, 4001), 4):
            yield {'x': combination[0], 'm': combination[1], 'a': combination[2], 's': combination[3]}

    #general_file parser
    def get_sum_of_all_ratings(self, file_name):
        sum_of_parts_rating_one = 0

        is_workflows = True
        for line in FileReader.gen_file_reader(file_name):
            if not line:
                is_workflows = False

            if is_workflows:
                key, rule = line.rstrip('}').split('{')
                self.workflows_dct[key] = rule
            
            if not is_workflows:
                if line:
                    parts_matches = re.findall(self.parts_patern, line)
                    parts_dict = {key: int(value) for key, value in parts_matches}
                    workflow_result = self.parts_workflow(part=parts_dict)
                    if workflow_result == 'A':
                        sum_of_parts_rating_one += sum(parts_dict.values())

        #task 2
        self.get_workflow_adj_list()
        accepted_conditions_path = self.bfs_to_find_possible_accepted_conditions()
        
        total_accepted_parts = 0
        for _, conditions in accepted_conditions_path:
            range_dict = {key: [1, 4000] for key in ['x', 'm', 'a', 's']}

            for variable_type, operator, value in conditions:
                if operator == '>':
                    range_dict[variable_type][0] = value + 1
                elif operator == '>=':
                    range_dict[variable_type][0] = value
                elif operator == '<':
                    range_dict[variable_type][1] = value - 1
                else:  # Assuming '='
                    range_dict[variable_type][1] = value

            total_accepted_parts += math.prod(range[1] - range[0] + 1 for range in range_dict.values())
        
        return sum_of_parts_rating_one, total_accepted_parts


if __name__ == '__main__':
    print('Day 19')
    parts_sorter_instance = PartsSorter()
    sum_of_ratings_part_1, total_accepted_parts_part_2 = parts_sorter_instance.get_sum_of_all_ratings(file_name='day_19.txt')
    print('Task 1 is = ', sum_of_ratings_part_1)
    print('Task 1 is = ', total_accepted_parts_part_2)