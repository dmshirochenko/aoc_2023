# https://adventofcode.com/2023/day/3

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class Scratchcards:
    def __init__(self):
        self.cards_instance = {}

    def get_sum_of_winning_combinations(self, file_name):
        sum_of_winning_combinations = 0
        card_num = 1

        for item in FileReader().gen_file_reader(file_name):
            card_game_number, combinations = item.split(": ")
            winning_combinations, numbers_to_check = combinations.split(" | ")

            winning_combinations_set = set(map(int, winning_combinations.split()))
            numbers_to_check_lst = list(map(int, numbers_to_check.split()))

            #add current card to intances
            self.cards_instance[card_num] = self.cards_instance.get(card_num, 0) + 1

            game_result = 0
            cards_won_lst = []

            for number in numbers_to_check_lst:
                if number in winning_combinations_set:
                    game_result = 1 if game_result == 0 else game_result * 2 #for task 1
                    cards_won_lst.append(card_num + len(cards_won_lst) + 1) #for task 2

            if card_num in self.cards_instance:
                for _ in range(self.cards_instance[card_num]):
                    for card in cards_won_lst:
                        self.cards_instance[card] = self.cards_instance.get(card, 0) + 1

            sum_of_winning_combinations += game_result
            card_num += 1


        return sum_of_winning_combinations


if __name__ == "__main__":
    print("Day 4")
    scratchcards_inst = Scratchcards()
    sum_of_winning_combinations = scratchcards_inst.get_sum_of_winning_combinations('day_4.txt')
    print('Task 1 = ', sum_of_winning_combinations)
    total_cards_num_sum = sum(scratchcards_inst.cards_instance.values())
    print('Task 2 = ', total_cards_num_sum)

"""
Task 1 =  17803
Task 2 =  5554894
"""