from tornado.escape import json_encode, json_decode
from Classes.Hand import *
from Classes.Deck import Deck


class Client:
    def __init__(self):
        self.rank = None
        self.suit = None
        self.username = None
        self.hand = Hand()
        self.id = None
        self.ws_connection = None
        self.deck = None

    def set_deck(self, deck):
        self.deck = deck

    def authorization(self, data=None):
        if data:
            print("auth data --> {}".format(data))
            self.set_deck(self.application.deck)
            self.username = data['username']
            self.send_message({"type": "id", "client_id": self.id})
            self.send_messages({"type": "new_client", "message": self.id}, extends=[self.id])
            return

        self.send_messages({"type": "auth"})

    def give_card(self):
        card_name = self.deck.deal_card()
        self.hand.add_card(card_name)
        print(card_name)
        print(self.hand.get_value())
        if self.hand.get_value() > 21:
            self.send_message({"type": "bust"})

        return str(card_name)



