import random


class Deck(object):
    """ Колода """

    def __init__(self):
        # ранги
        ranks = "23456789tjqka"
        # масти
        suits = "dchs"
        # генератор списков создающий колоду из 52 карт
        self.cards = [(s, r) for r in ranks for s in suits]
        # перетасовываем колоду. Не забудьте импортировать функцию shuffle из модуля random
        random.shuffle(self.cards)

    def deal_card(self):
        """ Функция сдачи карты """
        card = self.cards.pop(-1)
        card_name = card[1] + card[0]
        return card[1], card[0]

