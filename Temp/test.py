import random


# CLICKED += 1
def hit_card():
    ranks = "23456789tjqka"
    suits = "dchs"
    cards = [(s, r) for r in ranks for s in suits]
    random.shuffle(cards)
    card_name = str(cards[-1][0] + cards[-1][1])
    return card_name

