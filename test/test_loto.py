from loto_games import (check_played_players, get_bag_number, Player, Card)


class TestBagGenerator:
    bag = {balls: number for balls, number in get_bag_number()}

    def test_bag(self):
        assert len(self.bag) == 90

    def test_wrong_len_bag(self):
        assert not len(self.bag) == 91


class TestPlayerClass:
    test_player = Player.create_real_player("test")
    test_player.card.card_number = {1: "test"}
    test_player.card.outside_numbers = [1]

    def test_create_real_player(self):
        test_player = Player.create_real_player("test")
        assert test_player.player == "real"

    def test_create_computer_player(self):
        new_player = Player.create_computer_player("test")
        assert new_player.player == "computer"

    def test_check_number_in_card(self):
        assert self.test_player.check_number_in_card(1)

    def test_not_number_in_card(self):
        assert not self.test_player.check_number_in_card(2)

    def test_winners(self):
        self.test_player.check_winners()
        assert self.test_player.winner
        assert not self.test_player.played

    def test_check_played_players(self):
        assert check_played_players([self.test_player])


class TestCard:
    test_card = Card()

    def test_update_outside_numbers(self):
        self.test_card.updated_outside_numbers(1)
        assert len(self.test_card.outside_numbers) == 1


