from Classes.Hand import *
from Classes.Client import *


class Dealer:
    def __init__(self, deck):
        self.rank = None
        self.suit = None
        self.hand_dealer = Hand()
        self.id = "Dealer"
        self.points = None
        self.deck = deck

    def check_value(self):
            return self.hand_dealer.get_value()

    def give_card(self):
        card_name = self.deck.deal_card()
        self.hand_dealer.add_card(card_name)
        self.points = self.hand_dealer.get_value()
        # print(self.points)
        # print(self.hand_dealer)
        return str(card_name)

    def check_points(self):
        return int(self.points)