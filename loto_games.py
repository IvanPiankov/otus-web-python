from dataclasses import dataclass
import random
from typing import Generator


@dataclass
class Number:
    """ Data class for saving information about numbers on card_number"""
    line: int
    position: int


class Card:
    """ Class for bingo balls card"""
    def __init__(self):
        self.card_number = self._create_cards()
        self.card_view = self._card_view()
        self.outside_numbers = []

    def updated_outside_numbers(self, number: int):
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
        card_position = [[" "] * 10 for _ in range(3)]
        for number, data_number in self.card_number.items():
            card_position[data_number.line][data_number.position] = number
        return card_position

    def cross_out_number(self, number: int):
        if number in self.card_number:
            data_number = self.card_number[number]
            self.card_view[data_number.line][data_number.position] = "-"

    def update_card(self, number: int):
        self.cross_out_number(number)
        self.updated_outside_numbers(number)

    def __str__(self):
        position_to_line = [" ".join(map(str, line)) for line in self.card_view]
        return "\n".join(position_to_line)


class Player:
    """Class for gamers, which will be played in this game"""
    def __init__(self, type_player: str, name: str):
        self.card = Card()
        self.winner = False
        self.played = True
        self.player = type_player
        self.name = name

    def check_number_in_card(self, number: int):
        return number in self.card.card_number

    def check_winners(self):
        if len(self.card.card_number) == len(self.card.outside_numbers):
            self.winner = True
            self.played = False

    @classmethod
    def create_computer_player(cls, name: str):
        return cls("computer", name)

    @classmethod
    def create_real_player(cls, name: str):
        return cls("real", name)


def check_played_players(gamers: list) -> bool:
    played_gamers = len([gamer for gamer in gamers if gamer.played])
    return played_gamers < 2


def get_bag_number() -> Generator:
    bag_ball = list(range(1, 91))
    random.shuffle(bag_ball)
    number_bingo_balls = 89
    for bingo_balls in bag_ball:
        yield bingo_balls, number_bingo_balls
        number_bingo_balls -= 1


def get_card_gamers(gamers: list):
    for gamer in gamers:
        if not gamer.winner:
            print(f"Карточка игрока: {gamer.name}\n")
            print(gamer.card)


def main():
    # part with function for creating players
    print("Приветствуем Вас в игре Loto\n"
          "Ответьте на пару вопросов")
    all_players = int(input("Какое будет количество игроков ? : "))
    if all_players < 2:
        raise ValueError("Введено не корректное число игроков ")
    real_player = int(input("Сколько будет реальных игроков ? : "))
    assert real_player <= all_players, ValueError("Введено не корректное число игроков ")
    computer_player = 0
    if real_player < all_players:
        computer_player = all_players - real_player
    print(f"Игроков под упаравлением компьютера будет  - {computer_player}")
    assert computer_player + real_player == all_players, ValueError("Введено не корректное число игроков ")
    gamers = []
    # create players
    if real_player:
        for player in range(real_player):
            player_name = str(input("Введите имя игрока: "))
            gamers.append(Player.create_real_player(player_name))
    if computer_player:
        for player in range(computer_player):
            gamers.append(Player.create_computer_player("computer" + str(player + 1)))
    for bingo_ball, number_bingo_balls in get_bag_number():
        player_lose_in_session = False
        player_winners_in_session = False
        print(f"\nНовый бочонок: {bingo_ball}, Осталось: {number_bingo_balls}\n")
        get_card_gamers(gamers)
        for gamer in gamers:
            if not gamer.winner:
                if gamer.player != "computer":
                    answer = str(input('Зачеркнуть цифру? (y/n)'))
                    if answer == 'y':
                        if gamer.check_number_in_card(bingo_ball):
                            gamer.card.update_card(bingo_ball)
                        else:
                            gamer.played = False
                            print(f"Игрок с именем: {gamer.name} проиграл (")
                            player_lose_in_session = True
                    else:
                        if gamer.check_number_in_card(bingo_ball):
                            gamer.played = False
                            print(f"Игрок с именем: {gamer.name} проиграл (")
                            player_lose_in_session = True
                else:
                    if gamer.check_number_in_card(bingo_ball):
                        gamer.card.update_card(bingo_ball)
                gamer.check_winners()
                if gamer.winner:
                    print(f"Поздравляем игрока {gamer.name} c победой !")
                    player_winners_in_session = True
        if player_winners_in_session or player_lose_in_session:
            if check_played_players(gamers):
                break

    print('Игра окончена')


if __name__ == '__main__':
    main()
