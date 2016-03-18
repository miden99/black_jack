import json

import pygame

# from pgu import gui
import threading
import websocket
from client.Classes.PyMain import PyMain
from client.Classes.LoginForm import LoginForm
from client.Classes.ConnectForm import ConnectForm
from client.Classes.TestMessageForm import TestMessageForm
from Temp.SelectForm import SelectForm
from client.ws_events import *


def on_data(cls, data, opcode, fin):
    # TODO: добавить обработку ошибок при некорректной data
    data = json.loads(data)
    # print("data = ", data)
    if data.get("type") == "error":
        on_errors('', data)
    custom_event = pygame.event.Event(WS_MESSAGE, data=data, test=0)
    pygame.event.post(custom_event)


def on_errors(cls, error):
    print("error = ", error)
    custom_event = pygame.event.Event(WS_ERROR, error=error)
    pygame.event.post(custom_event)


if __name__ == "__main__":
    # Инициализируем веб-соккет
    ws = websocket.WebSocketApp("ws://127.0.1.1:8888/websocket", on_data=on_data, on_error=on_errors)

    main_window = PyMain()
    login_form = LoginForm((20, 20), main_window.screen, ws=ws)
    connect_form = ConnectForm((20, 20), main_window.screen, ws=ws)
    tm_form = TestMessageForm((20, 150), main_window.screen, ws=ws)
    select_form = SelectForm((120, 150), main_window.screen)
    main_window.add_render_object(login_form)
    main_window.add_render_object(connect_form)
    main_window.add_render_object(tm_form)
    main_window.add_render_object(select_form)
    main_thread = threading.Thread(target=main_window.loop)

    main_thread.start()
