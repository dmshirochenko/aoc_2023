# https://adventofcode.com/2023/day/9


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class InstabilitySensor:
    def __init__(self):
        pass

    def get_first_and_last_digits_from_sequence(self, result_to_analyze):
        last_numbers_in_seq = [result_to_analyze[-1]]
        first_numbers_in_seq = [result_to_analyze[0]]
        is_all_zeros = False
        curr_temp_lst_to_check = result_to_analyze

        while not is_all_zeros:
            new_temp_lst_to_check = []

            is_all_zeros = True
            for i in range(1, len(curr_temp_lst_to_check)):
                new_value = curr_temp_lst_to_check[i] - curr_temp_lst_to_check[i - 1]
                new_temp_lst_to_check.append(new_value)
                if is_all_zeros and new_value != 0:
                    is_all_zeros = False

            first_numbers_in_seq.append(new_temp_lst_to_check[0])
            last_numbers_in_seq.append(new_temp_lst_to_check[-1])
            curr_temp_lst_to_check = new_temp_lst_to_check

        return first_numbers_in_seq, last_numbers_in_seq

    def get_predicted_value(self, result_to_analyze):
        first_numbers_in_seq, last_numbers_in_seq = self.get_first_and_last_digits_from_sequence(result_to_analyze)

        # task 1
        predicted_num_last = sum(last_numbers_in_seq)

        # task 2
        predicted_num_first = 0
        for i in range(len(first_numbers_in_seq) - 2, -1, -1):
            predicted_num_first = first_numbers_in_seq[i] - predicted_num_first

        return predicted_num_first, predicted_num_last

    def get_result_prediction_sum(self, file_name):
        sum_of_predisctions_first = 0
        sum_of_predisctions_last = 0

        for line in FileReader().gen_file_reader(file_name):
            result_to_analyze = [int(i) for i in line.split()]
            predicted_num_first, predicted_num_last = self.get_predicted_value(result_to_analyze)

            sum_of_predisctions_first += predicted_num_first
            sum_of_predisctions_last += predicted_num_last

        return sum_of_predisctions_first, sum_of_predisctions_last


if __name__ == "__main__":
    print("Day 9")
    instability_sensor_instance = InstabilitySensor()
    sum_of_predisctions_first, sum_of_predisctions_last = instability_sensor_instance.get_result_prediction_sum(
        "day_9.txt"
    )
    print("Task 1 = ", sum_of_predisctions_last)
    print("Task 2 = ", sum_of_predisctions_first)
