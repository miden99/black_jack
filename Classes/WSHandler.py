import tornado.websocket
from Classes.Dealer import Dealer
from tornado.escape import json_encode, json_decode
from Classes.Client import Client
from Classes.Deck import Deck


# Список кодов состояния HTTP:
# https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP
class WSHandler(tornado.websocket.WebSocketHandler, Client):
    def open(self):
        """
        Вызывается при подключении нового клиента
        Присваивание клиенту id
        """
        print('new connection')
        if len(self.application.webSocketsPlayers) < 3:
            # self.id
            # length = len(self.application.webSocketsPlayers)
            if self.application.webSocketsPlayers:
                self.id = self.application.webSocketsPlayers[-1].id + 1
            else:
                self.id = 1
            self.application.webSocketsPlayers.append(self)
            self.authorization()
        else:
            self.send_error(status_code=507, message='all busy')

    def on_message(self, message):
        """
        Вызывается при получении сообщения от клиента
        """
        print("players = ", self.application.webSocketsPlayers)

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

        if not self.in_game:
            # TODO(+): отправить сообщение об ошибке
            self.send_error(status_code=666, message='ход закончен')
            return
        if message.get('type') == 'hit':
            self.send_messages({"type": "hit", "card": self.give_card(), "id": self.id, "points": self.hand.get_value()})
            self.check_value()

        elif message.get('type') == 'stand':
            self.in_game = False
        #
        if self.end_current_game():
            dealer = self.application.dealer
            # TODO: тут начинаем новую игру: тусуем колоду, очищаем руки игроков и т.д.
            while dealer.check_value() < 17:
                self.send_messages({"type": "hit", "card":  dealer.give_card(),
                                    "id": dealer.id,
                                    "points": dealer.check_value()})
            if dealer.check_value() > 21:
                max_result = 0
                id_winner = 0
                for player in self.application.webSocketsPlayers:
                    if player.points >= max_result and player.points != 0:
                        max_result = player.points
                        id_winner = player
                id_winner.send_message({"type": "winner", "id": id_winner.id})
                id_winner.send_messages({"type": "lose"}, extends=id_winner)
            else:
                max_result = 0
                id_winner = 0
                for player in self.application.webSocketsPlayers:
                    if player.points >= max_result and player.points != 0:
                        max_result = player.points
                        id_winner = player
                if id_winner.points > dealer.points:
                    id_winner.send_message({"type": "winner", "id": id_winner.id})
                    id_winner.send_messages({"type": "lose"}, extends=id_winner)
                else:
                    id_winner.send_messages({"type": "lose"})

            print("GGG")

    def end_current_game(self):
        # TODO(~+): проверяет все in_game игроков
        for player in self.application.webSocketsPlayers:
            if player.in_game is True:
                return False

        return True


        # for value in self.application.webSocketsPlayers:
        #     if value != self:
        #         print('send -->', message)
        #         value.ws_connection.write_message(message)

    def send_error(self, status_code=500, message=''):
        self.ws_connection.write_message(json_encode({"type": "error", "status_code": status_code, "message": message}))
        
        # self.send_messages("Hello", extends=[self.id])
        # self.send_messages("Hello", extends=[1, 2])

    def send_message(self, message):
        """
        Отправляет сообщение текущему
        """
        self.ws_connection.write_message(json_encode(message))

    def send_messages(self, message, extends=[]):
        """
        Отправляет сообщение всем Юзерам, кроме списка исключений
        extends: список id
        """
        for user in self.application.webSocketsPlayers:
            if user.id in extends:
                continue
            user.ws_connection.write_message(json_encode(message))

    # def send_message(self, message):
    #     """
    #     Отправляет сообщение всем Юзерам
    #     """
    #     for el in self.application.webSocketsPlayers:
    #         el.ws_connection.write_message(json_encode(message))
    # 
    # def send_message_one_user(self, message):
    #     """
    #     Отправляет сообщение текущему
    #     """
    #     self.ws_connection.write_message(json_encode(message))
    # 
    # def send_message_user(self, message):
    #     """
    #     Отправляет всем, кроме текущего
    #     """
    #     for el in self.application.webSocketsPlayers:
    #         if self.ws_connection is not el.ws_connection:
    #             el.ws_connection.write_message(json_encode(message))

    def on_close(self):
        """
        Вызывается при отключении клиента
        """
        print('connection closed')
        for key, value in enumerate(self.application.webSocketsPlayers):
            if value == self:
                del self.application.webSocketsPlayers[key]

    def __repr__(self):
        return "Client name: {}".format(self.username or 'unregistered')

    def check_origin(self, origin):
        return True
