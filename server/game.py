from server.api import BaseHandler


class PongBot(BaseHandler):
    def process_game_state(self, game_state):
        pass

    def after_close(self):
        pass

    def choose_move(self, data: dict):
        player = data['playerId']
        state = data['state']

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

        return {'move': move, 'start': 1}
