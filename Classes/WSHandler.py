import tornado.websocket
from tornado.escape import json_encode, json_decode
from Classes.Client import Client
import random


# Список кодов состояния HTTP:
# https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP
class WSHandler(tornado.websocket.WebSocketHandler, Client):
    def open(self):
        """
        Вызывается при подключении нового клиента
        Присваивание клиенту id
        """
        print('new connection')
        if len(self.application.webSocketsPool) < 2:
            # self.id
            # length = len(self.application.webSocketsPool)
            if self.application.webSocketsPool:
                self.id = self.application.webSocketsPool[-1].id + 1
            else:
                self.id = 1
            self.application.webSocketsPool.append(self)
            self.authorization()
        else:
            self.send_error(status_code=507, message='all busy')

    def on_message(self, message):
        """
        Вызывается при получении сообщения от клиента
        """
        print(self.application.webSocketsPool)

        try:
            message = json_decode(message)
        except ValueError:
            self.send_error(status_code=400, message='data not json')
            return
        print("message --> :", message)
        if message.get("type") == "auth":
            self.authorization(message["data"])
        else:
            if self.username is None:
                self.send_error(status_code=401, message='не авторизован')
                return
        if len(self.application.webSocketsPool) < 2:
            self.send_error(status_code=000, message="please wait")
        else:
            if message.get('type') == 'hit':
                ranks = "23456789tjqka"
                suits = "dchs"
                cards = [(s, r) for r in ranks for s in suits]
                random.shuffle(cards)
                card_name = str(cards[-1][0] + cards[-1][1])
                self.send_message({"type": "hit", "message": card_name, "id": self.id})


        # for value in self.application.webSocketsPool:
        #     if value != self:
        #         print('send -->', message)
        #         value.ws_connection.write_message(message)

    def send_error(self, status_code=500, message=''):
        self.ws_connection.write_message(json_encode({"type": "error", "status_code": status_code, "message": message}))

    def send_message(self, message):
        for el in self.application.webSocketsPool:
            el.ws_connection.write_message(json_encode(message))

    def send_message_one_user(self, message):
        self.ws_connection.write_message(json_encode(message))

    def on_close(self):
        """
        Вызывается при отключении клиента
        """
        print('connection closed')
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]

    def __repr__(self):
        return "Client name: {}".format(self.username or 'unregistered')
