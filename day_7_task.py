# https://adventofcode.com/2023/day/7
import re


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class CamelCards:
    def __init__(self):
        self.cards_combination_map = {
            "five_of_kind": [],
            "four_of_kind": [],
            "full_house": [],
            "three_of_kind": [],
            "two_pair": [],
            "one_pair": [],
            "high_card": [],
        }

        self.cards_ranking = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11,
            "T": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2,
        }

    def sort_hands_by_highest_card(self, hands, is_part_two=False):
        # condition for part 2
        if is_part_two:
            self.cards_ranking["J"] = 1

        def hand_rank(hand):
            return tuple(self.cards_ranking.get(card, 0) for card in hand if card in self.cards_ranking)

        hands.sort(key=lambda x: hand_rank(x[0]), reverse=True)

    def sort_hands_by_type(self, hand, bid, is_part_two=False):
        hand_map = dict()
        for card in hand:
            if card not in hand_map:
                hand_map[card] = 1
            else:
                hand_map[card] += 1

        sorted_hands = sorted(hand_map.values(), reverse=True)
        if is_part_two:
            num_of_jacks = hand_map.get("J")
            if num_of_jacks:
                if num_of_jacks == 4:
                    sorted_hands[0] = 5
                elif num_of_jacks == 3:
                    if sorted_hands[1] == 2:
                        sorted_hands[0] = 5
                    else:
                        sorted_hands[0] = 4
                elif num_of_jacks == 2:
                    if sorted_hands[0] == 3:
                        sorted_hands[0] = 5
                    elif sorted_hands[0] == 2 and sorted_hands[1] == 2:
                        sorted_hands[0] = 4
                    else:
                        sorted_hands[0] = 3
                        sorted_hands[1] = 1
                elif num_of_jacks == 1:
                    sorted_hands[0] += 1

        if sorted_hands[0] == 5:
            self.cards_combination_map["five_of_kind"].append((hand, bid))
        elif sorted_hands[0] == 4:
            self.cards_combination_map["four_of_kind"].append((hand, bid))
        elif sorted_hands[0] == 3 and sorted_hands[1] == 2:
            self.cards_combination_map["full_house"].append((hand, bid))
        elif sorted_hands[0] == 3 and sorted_hands[1] == 1:
            self.cards_combination_map["three_of_kind"].append((hand, bid))
        elif sorted_hands[0] == 2 and sorted_hands[1] == 2:
            self.cards_combination_map["two_pair"].append((hand, bid))
        elif sorted_hands[0] == 2 and sorted_hands[1] == 1:
            self.cards_combination_map["one_pair"].append((hand, bid))
        else:
            self.cards_combination_map["high_card"].append((hand, bid))

    def get_hands_rank(self, file_name, is_part_two=False):
        final_sum_of_ranks = 0
        num_of_hands = 0
        # sort by hand's combination
        for line in FileReader().gen_file_reader(file_name):
            hand, bid = line.split()
            self.sort_hands_by_type(hand, int(bid), is_part_two)
            num_of_hands += 1

        # sort by highest card
        for hands in self.cards_combination_map.values():
            if hands:
                self.sort_hands_by_highest_card(hands, is_part_two)
                for hand, bid in hands:
                    final_sum_of_ranks += bid * num_of_hands
                    num_of_hands -= 1

        return final_sum_of_ranks


if __name__ == "__main__":
    print("Day 7")
    camal_game_instance_part_1 = CamelCards()
    final_card_score_part_1 = camal_game_instance_part_1.get_hands_rank("day_7.txt")
    print("Task 1 =", final_card_score_part_1)
    camal_game_instance_part_2 = CamelCards()
    final_card_score_part_2 = camal_game_instance_part_2.get_hands_rank(file_name="day_7.txt", is_part_two=True)
    print("Task 2 =", final_card_score_part_2)
