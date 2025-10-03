from typing import Any

from src.socket_data import SocketData
from src.api import BaseHandler



class PongBot(BaseHandler):
    def process_game_state(self, game_state: SocketData):
        print(f"Received game state: {game_state}")

    def after_close(self):
        print(f"WebSocket connection closed")
        pass

    def choose_move(self, data: SocketData) -> dict[str, Any]:
        player = data.playerId
        state = data.state

        if player == 0:
            if state['ballY'] < state['leftPaddleY'] + 50:
                move = 1
            else:
                move = -1
        else:
            if state['ballY'] < state['rightPaddleY'] + 50:
                move = 1
            else:
                move = -1

        move = {'move': move, 'start': 1}
        print(f"Choosing move: {move}")

        return move
