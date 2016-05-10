import random
from Classes.Hand import Card

class Deck(object):
    """ Колода """

    def __init__(self):
        # ранги
        ranks = "23456789tjqka"
        # масти
        suits = "dchs"
        # генератор списков создающий колоду из 52 карт
        self.cards = [Card(r, s) for r in ranks for s in suits]
        # перетасовываем колоду. Не забудьте импортировать функцию shuffle из модуля random
        random.shuffle(self.cards)

    def deal_card(self):
        """ Функция сдачи карты """
        return self.cards.pop(-1)

