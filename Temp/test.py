class Hand(object):
    """ Рука """

    def __init__(self, name):
        # имя игрока
        self.name = name
        # Изначально рука пустая
        self.cards = []

    def add_card(self, card):
        """ Добавляет карту на руку """
        self.cards.append(card)

    def get_value(self):
        """ Метод получения числа очков на руке """
        result = 0
        # Количество тузов на руке.
        aces = 0
        for card in self.cards:
            result += card.card_value()
            # Если на руке есть туз - увеличиваем количество тузов
            if card.get_rank() == "A":
                aces += 1
        # Решаем считать тузы за 1 очко или за 11
        if result + aces * 10 <= 21:
            result += aces * 10
        return result

    def __str__(self):
        text = "%s's contains:\n" % self.name
        for card in self.cards:
            text += str(card) + " "
        text += "\nHand value: " + str(self.get_value())
        return text

class Card:
    """ Карты """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.card_name = str(suit + rank) + '.png'
        # FIXME: загружать карты в соответствии с парметрами
        self.image = load_image(path="images/cards", name=self.card_name)

    def card_value(self):
        """ Возращает количество очков которое дает карта """
        if self.rank in "TJQK":
            # По 10 за десятку, валета, даму и короля
            return 10
        else:
            # Возвращает нужное число очков за любую другую карту
            # Туз изначально дает одно очко.
            return " A23456789".index(self.rank)

    def get_rank(self):
        return self.rank

    def render(self, screen, pos):
        screen.blit(self.image, pos)

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)