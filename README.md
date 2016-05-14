## About project
Тут будет описание проекта
## Run project
### install requirements
#### 1. Install pip:
    sudo apt-get install python3-pip
    //Для устоновки прочих библиотек

#### 2. Install pygame (on linux)//Client:
    sudo apt-get build-dep python-pygame,
    sudo apt-get install mercurial,
    On Windows you can use the installer: http://mercurial.selenic.com/wiki/Download
    
    Use pip to install PyGame:
    pip install hg+http://bitbucket.org/pygame/pygame,
    If the above gives freetype-config: not found error (on Linux), then try sudo apt-get install libfreetype6-dev and then repeat 3.

#### 3. Install tornado
    sudo pip3 install tornado
    
#### 4.~api~
    Подключение
        Сервер ожидает:
            Обращения клиента
    
        Сервер отправляет:
            {"type": "auth"} -
    
            В случае ошибки сервер отправляет:
                {"status_code" 507, "message": 'all busy')  //("Мест нет")//


    Авторизация
        Сервер ожидает:
            {"type": "auth", "data": {"username": <username>}}
    
        Сервер отправляет self:
            // {"type": "client_id", "message": <client_id>}
            {"type": "id", "client_id": <client_id>}
            Дважды:
            {"type": "hit", "card": <card>, "id": <id>, "points": <points>}
            Также информацию о игроках подключившихся раньше, если таковые имеются
            {"type":"other_hands", "hand":<карты на руке>, "id": <id руки>, "ponts": <его очки>}

    
        Сурвер отвравляет остальным(при успешной авторизации self):
            {"type": "new_client", "message": <other_id>}
    
        Ошибки возникают в случае
        Отсутствие авторизации пользователем:
        Сервер отправляет
            {"status_code": 401, "message": 'не авторизован'}
     
            
    Запрос карт 
        Сервер ожидает:
           {"type": "hit"}
           
        Сервер отправляет:
           {"type": "hit", "card": <card>, "id": <id запросившего>, "points": <очки запросившего>}}
           
           
    В случае перебора карт сервер отправляет клиенту:
        {"type": "bust"}

    Для того чтобы закончить ход клиент отправляет:
        {"type": "stand"}