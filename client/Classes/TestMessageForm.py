from pgu import gui
from .GUIWrapper import GUIWrapper
from ..ws_events import *
import json


class TestMessageForm(GUIWrapper):
    size = (200, 50)
    visible = True

    def __init__(self, pos, screen, ws):
        # Веб-сокет
        self.ws = ws
        GUIWrapper.__init__(self, pos, screen)

    def create_components(self):
        self.message_field = gui.Input()
        button_send = gui.Button('Send')
        button_send.connect(gui.CLICK, self.send_message, '')
        table = gui.Table()
        table.tr()
        table.td(gui.Label("message: "))
        table.td(self.message_field)
        table.tr()
        table.td(button_send, colspan=2)
        self.pack_manager = table

    def send_message(self, _):
        self.ws.send(json.dumps({"message": self.message_field.value}))