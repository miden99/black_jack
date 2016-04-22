from tornado.escape import json_encode, json_decode


class Client:
    def __init__(self):
        self.username = None
        self.hand = []
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


