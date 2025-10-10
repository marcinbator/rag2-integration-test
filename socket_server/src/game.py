from typing import Any

from src.game_state import GameState
from src.api import BaseWebSocketHandler



class PongWebSocketHandler(BaseWebSocketHandler):
    def on_open(self):
        print("Websocket pong connection opened")

    def process_game_state(self, game_state: GameState):
        print(f"Received pong game state: {game_state}")

    def choose_move(self, data: GameState) -> dict[str, Any]:
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
