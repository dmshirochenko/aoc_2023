# https://adventofcode.com/2023/day/1


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class CalibrationRestorer:
    def __init__(self):
        self.dict_coord = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

    def calibration(self, file_name):
        digits = []
        for row in FileReader.gen_file_reader(file_name):
            digits_in_row = []
            for char in row:
                if char.isdigit():
                    digits_in_row.append(char)

            digit_to_add = int(digits_in_row[0] + digits_in_row[-1])
            digits.append(digit_to_add)

        return digits

    def calibration_advanced(self, file_name):
        digits = []
        for row in FileReader.gen_file_reader(file_name):
            digits_in_row = []
            left = 0

            while left < len(row):
                if row[left].isdigit():
                    digits_in_row.append(row[left])
                    left += 1
                    continue

                for key, value in self.dict_coord.items():
                    key_len = len(key)
                    try:
                        if row[left : left + key_len] == key:
                            digits_in_row.append(value)
                            break
                    except:
                        pass

                left += 1

            digit_to_add = int(digits_in_row[0] + digits_in_row[-1])
            digits.append(digit_to_add)

        return digits


if __name__ == "__main__":
    calibrator = CalibrationRestorer()
    # task 1
    coordinates = calibrator.calibration("day_1.txt")
    sum_of_coord = 0
    for coor in coordinates:
        sum_of_coord += coor
    print("Task one is = ", sum_of_coord)

    # task 2
    coordinates_advance = calibrator.calibration_advanced("day_1.txt")
    sum_of_coord_adv = 0
    for coor in coordinates_advance:
        sum_of_coord_adv += coor
    print("Task two is = ", sum_of_coord_adv)
