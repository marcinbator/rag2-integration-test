from flask import Flask, request, jsonify
from flask_cors import CORS


class DataServer:    
    def __init__(self, host='0.0.0.0', port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.data_storage = []
        
        self._register_routes()
    
    def _register_routes(self):
        self.app.add_url_rule('/data', 'receive_data', self.receive_data, methods=['POST'])
        self.app.add_url_rule('/data', 'get_all_data', self.get_all_data, methods=['GET'])
        self.app.add_url_rule('/data/<int:data_id>', 'get_data_by_id', self.get_data_by_id, methods=['GET'])
    
    def receive_data(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"status": "error", "message": "No data provided"}), 400
            
            self.data_storage.append(data)
            print(f"Received data: {data}")
            
            return jsonify({"status": "success", "message": "Data received successfully"}), 200
        
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    def get_all_data(self):
        try:
            return jsonify({
                "status": "success",
                "data": self.data_storage,
                "count": len(self.data_storage)
            }), 200
        
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    def get_data_by_id(self, data_id):
        try:
            if 0 <= data_id < len(self.data_storage):
                return jsonify({
                    "status": "success",
                    "data": self.data_storage[data_id],
                    "id": data_id
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": f"No data found for id {data_id}"
                }), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    def run(self):        
        self.app.run(host=self.host, port=self.port, debug=self.debug)



if __name__ == '__main__':
    server = DataServer(host='0.0.0.0', port=8080, debug=False)
    server.run()
