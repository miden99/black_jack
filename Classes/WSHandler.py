import tornado.websocket
from tornado.escape import json_encode, json_decode
from Classes.Client import Client


# Список кодов состояния HTTP:
# https://ru.wikipedia.org/wiki/Список_кодов_состояния_HTTP
class WSHandler(tornado.websocket.WebSocketHandler, Client):
    def open(self):
        """
        Вызывается при подключении нового клиента
        """
        print('new connection')
        if len(self.application.webSocketsPool) < 2:

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
            if not self.username:
                self.send_error(status_code=401, message='не авторизован')
        # for value in self.application.webSocketsPool:
        #     if value != self:
        #         print('send -->', message)
        #         value.ws_connection.write_message(message)

    def send_error(self, status_code=500, message=''):
        self.ws_connection.write_message(json_encode({"type": "error", "status_code": status_code, "message": message}))

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
