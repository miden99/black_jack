import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
from Classes.WSHandler import WSHandler
from Classes.Deck import Deck


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPlayers = []
        self.deck = Deck()

        handlers = [
            (r'/websocket', WSHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    # myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***')
    tornado.ioloop.IOLoop.instance().start()
