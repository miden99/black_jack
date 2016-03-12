from tornado.escape import json_encode, json_decode


class Client:
    def __init__(self):
        self.username = None
        self.hand = []
        # self.auth = False
        self.ws_connection = None

    def authorization(self, data=None):
        if data:
            print("auth data --> {}".format(data))
            self.username = data['username']
            # self.auth = True
            return

        self.send_message({"type": "auth"})
