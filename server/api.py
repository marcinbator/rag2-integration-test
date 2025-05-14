import json
import os
import time
from abc import abstractmethod
from typing import final, Any
from urllib.parse import urlparse, parse_qs

import requests
from dotenv import load_dotenv
from tornado.websocket import WebSocketHandler

from server.socket_data import SocketData

guest_users = 0


def verify_jwt(token):
    if os.getenv("PRODUCTION", 'false').lower() == "false":
        return True

    load_dotenv()
    TOKEN_VERIFY_URL = os.getenv('TOKEN_VERIFY_URL')
    headers = {"Authorization": "Bearer " + token}

    try:
        response = requests.get(TOKEN_VERIFY_URL, headers=headers, timeout=2)
        print(response)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"JWT verification failed: {e}")
        return False


class BaseHandler(WebSocketHandler):
    is_guest = False
    last_message_time = None

    @final
    def check_origin(self, origin):
        load_dotenv()
        allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:4200,http://rutai.kia.prz.edu.pl')

        allowed_origins_list = allowed_origins.split(',')
        if origin in allowed_origins_list:
            return True
        print(f"Origin {origin} not allowed")
        return False

    @final
    def open(self):
        global guest_users

        query_params = parse_qs(urlparse(self.request.uri).query)
        token = query_params.get("jwt", [None])[0]
        load_dotenv()
        ALLOWED_GUEST_USERS = os.getenv('ALLOWED_GUEST_USERS', 5)

        if not token or not verify_jwt(token):
            if guest_users >= int(ALLOWED_GUEST_USERS):
                print("Max guest limit exceeded")
                self.close()
                return
            guest_users += 1
            self.is_guest = True
            print("WebSocket connection opened as guest")
        else:
            self.is_guest = False
            print("WebSocket connection opened as authenticated")

    @final
    def on_close(self):
        global guest_users

        if self.is_guest:
            guest_users -= 1
            print(f"Guest user disconnected. Remaining guest users: {guest_users}")
        else:
            print("User disconnected")

        self.after_close()

    @final
    def on_message(self, message):
        if self.last_message_time is not None and time.time() - self.last_message_time <= 0.045: return
        self.last_message_time = time.time()

        game_state_json = json.loads(message)
        game_state = SocketData(**game_state_json)
        self.process_game_state(game_state)

        move = self.choose_move(game_state)
        self.write_message(json.dumps(move))

    @abstractmethod
    def process_game_state(self, game_state: SocketData):
        pass

    @abstractmethod
    def choose_move(self, data: SocketData) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def after_close(self):
        pass
