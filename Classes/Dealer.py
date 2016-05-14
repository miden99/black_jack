from Classes.Hand import *
from Classes.Client import *

class Dealer:
    def __init__(self, deck):
        self.cards = []  # [Card(), Card(), ...]
        self.deck = deck

    @property
    def hand_points(self):
        return None

    def add_cards(self):
        # Добавляет карту диллеру
        card = Card(*self.deck.deal_card())
        self.cards.append(card)

    # @property
    # def dealer_step(self):
    #     while self.cards.get_value() > 17:
    #         self.cards.add_cards
    #     return len(self.cards)