import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class DataHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            data = json.loads(post_data.decode('utf-8'))
            print(f"Received data")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "success", "message": "Data received successfully"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
    

def run_data_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, DataHandler)
    print(f"Data server started on port {port}")
    print("Endpoint available at: POST /data")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    run_data_server()
