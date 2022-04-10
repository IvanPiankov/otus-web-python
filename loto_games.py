import random
from dataclasses import dataclass
from copy import deepcopy

# TODO: Определить 5 классов:
# 1) Карточка TODO: Done
# 2) Игрок TODO: In progress
# 3) Мешок
# 4) Живой игрок
# 5) Компьютер

# TODO: Продумать методы и атрибоуты у классов.

# Начнем с кароточки


@dataclass
class Number:
    """ Data class for saving information about numbers on card_number"""
    line: int
    position: int


class Card:

    def __init__(self):
        self.card_number = self._create_cards()
        self.card_view = self._card_view()
        self.outside_numbers = []

    def updated_outside_numbers(self, number):
        self.outside_numbers.append(number)

    @staticmethod
    def _create_cards():
        # create all numbers for card_number
        all_numbers = random.sample(range(1, 91), 15)
        card_numbers = {}
        line = 0
        for numbers_slice in (all_numbers[start::3] for start in range(3)):
            # sort list
            numbers_slice.sort()
            all_position = sorted(random.sample(range(0, 10), 5))
            for number_index in range(len(numbers_slice)):
                card_numbers[numbers_slice[number_index]] = Number(line, all_position[number_index])
            line += 1
        return card_numbers

    def _card_view(self):
        # TODO: Придумать как все это решить меня не устраивает вид всего этого дела.
        f_l = [[" "] * 10]
        s_l = [[" "] * 10]
        t_l = [[" "] * 10]
        card_position = f_l + s_l + t_l
        for number, data_number in self.card_number.items():
            card_position[data_number.line][data_number.position] = number
        return card_position

    def cross_out_number(self, number):
        if number in self.card_number:
            data_number = self.card_number[number]
            self.card_view[data_number.line][data_number.position] = "-"
        # else:
        #     # create greate error type
        #     raise TypeError

    def __str__(self):
        position_to_line = [" ".join(map(str, line)) for line in self.card_view]
        return "\n".join(position_to_line)






def main():
    first_card = Card()
    second_card = Card()
    print(first_card)
    print("-------------" * 3)
    print(second_card)
    print("---NEW----------")
    first_card.cross_out_number(33)
    print(first_card)

    # print(first_card.card_number)
    # print(first_card.card_view)

    # print(second_card.card_number)


if __name__ == '__main__':
    main()