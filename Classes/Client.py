from tornado.escape import json_encode, json_decode
import random

class Client:
    def __init__(self):
        self.username = None
        self.hand = []
        self.ranks = "23456789tjqka"
        self.suits = "dchs"
        self.id = None
        # self.auth = False
        self.ws_connection = None

    def authorization(self, data=None):
        if data:
            print("auth data --> {}".format(data))
            self.username = data['username']
            self.send_message_one_user({"type": "id", "client_id": self.id})
            self.send_message_user({"type": "new_client", "message": self.id})
            return

        self.send_message({"type": "auth"})

    def give_card(self):
        cards = [(s, r) for r in self.ranks for s in self.suits]
        random.shuffle(cards)
        card_name = str(cards[-1][0] + cards[-1][1])
        return card_name
