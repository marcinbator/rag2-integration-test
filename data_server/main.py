from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from game_state import GameState


class GameRecordService:    
    def __init__(self, host='localhost', port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.game_states: list[GameState] = []
        
        self._register_routes()
    
    def _register_routes(self):
        self.app.add_url_rule('/game-states', 'receive_data', self.receive_data, methods=['POST'])
        self.app.add_url_rule('/game-states', 'get_all_data', self.get_all_data, methods=['GET'])
        self.app.add_url_rule('/game-states/<int:data_id>', 'get_data_by_id', self.get_data_by_id, methods=['GET'])
    
    def receive_data(self):
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        if "dataset" not in data or not isinstance(data["dataset"], list):
            return jsonify({
                "status": "error", 
                "message": "Invalid data format"
            }), 400
        
        dataset = data["dataset"]
        added_states = []
        
        for item in dataset:
            try:
                game_state = GameState(**item)
                self.game_states.append(game_state)
                added_states.append(len(self.game_states) - 1)
                print(f"Received game state: {game_state}")
            except ValidationError as e:
                print(f"Invalid game state data: {e}")
                continue
        
        return jsonify({
            "status": "success", 
            "message": "Game states received successfully",
            "ids": added_states,
            "processed": len(added_states),
            "total": len(dataset)
        }), 200
    
    def get_all_data(self):
        game_states_data = [game_state.model_dump() for game_state in self.game_states]
        
        return jsonify({
            "status": "success",
            "data": game_states_data,
            "count": len(self.game_states)
        }), 200
    
    def get_data_by_id(self, data_id):
        if 0 <= data_id < len(self.game_states):
            game_state = self.game_states[data_id]
            return jsonify({
                "status": "success",
                "data": game_state.model_dump(),
                "id": data_id
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"No game state found for id {data_id}"
            }), 404
    
    def run(self):        
        self.app.run(host=self.host, port=self.port, debug=self.debug)



if __name__ == '__main__':
    server = GameRecordService(host='localhost', port=8080, debug=False)
    server.run()
