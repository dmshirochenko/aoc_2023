# https://adventofcode.com/2023/day/15


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class Node:
    def __init__(self, label, focus_power):
        self.label = label
        self.focus_power = focus_power
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.total_focus_power = 0

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def append_or_update(self, label, focus_power):
        current_node = self.head
        while current_node:
            if current_node.label == label:
                current_node.focus_power = focus_power
                return
            current_node = current_node.next

        new_node = Node(label, focus_power)
        if self.head is None:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node

    def display(self):
        current_node = self.head
        while current_node:
            print(f"{current_node.label} (Focus Power: {current_node.focus_power})", end=" -> ")
            current_node = current_node.next
        print("None")

    def delete_node(self, key):
        current_node = self.head

        if current_node and current_node.label == key:
            self.head = current_node.next
            current_node = None
            return

        prev = None
        while current_node and current_node.label != key:
            prev = current_node
            current_node = current_node.next

        if current_node is None:
            return

        prev.next = current_node.next
        current_node = None


class HashFunc:
    def __init__(self):
        self.lenses_dict = {}

    def hash_function(self, text):
        HASH_MULTIPLIER = 17
        MODULUS = 256

        hash_result = 0
        for char in text:
            hash_result = (hash_result + ord(char)) * HASH_MULTIPLIER % MODULUS
        
        return hash_result

    def lenses_dict_implementation(self, text):
        if '-' in text:
            label = text.rstrip('-')
            label_hash = self.hash_function(label)
            if label_hash in self.lenses_dict:
                self.lenses_dict[label_hash].delete_node(label)

        else:
            label, focus_power = text.split('=')
            label_hash = self.hash_function(label)

            if label_hash not in self.lenses_dict:
                llist = LinkedList()
                llist.append_or_update(label=label, focus_power=int(focus_power))
                self.lenses_dict[label_hash] = llist
            else:
                self.lenses_dict[label_hash].append_or_update(label, int(focus_power))

    def get_sum_of_focusing_power_of_lenses(self):
        sum_of_focusing_power = 0

        for box_key, box_values in self.lenses_dict.items():
            multiplication_box_result = 0
            lens_counter = 1
            for lens in box_values:
                multiplication_box_result += (box_key + 1) * (lens_counter * lens.focus_power)
                lens_counter += 1

            sum_of_focusing_power += multiplication_box_result

        return sum_of_focusing_power

    def get_sum_of_hashes(self, file_name):
        sum_of_hashes = 0       
        lst_of_strings = [i for i in next(FileReader().gen_file_reader(file_name)).split(',')]
        
        for line in lst_of_strings:
            sum_of_hashes += self.hash_function(line)
            self.lenses_dict_implementation(line)

        return sum_of_hashes

if __name__ == '__main__':
    print('Day 15')
    hash_func_instance = HashFunc()
    sum_of_hashes = hash_func_instance.get_sum_of_hashes('day_15.txt')
    print('Task 1 = ', sum_of_hashes)
    sum_of_focusing_power = hash_func_instance.get_sum_of_focusing_power_of_lenses()
    print('Task 2 = ', sum_of_focusing_power)