import os
import re
import subprocess
import threading
import time
import sys

import tornado.ioloop
from dotenv import load_dotenv
from tornado.web import Application

from server.game import PongBot

YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TeeOutput:
    def __init__(self, file, original_stdout):
        self.file = file
        self.original_stdout = original_stdout
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def write(self, data):
        self.original_stdout.write(data)
        clean_data = self.ansi_escape.sub('', data)
        self.file.write(clean_data)
        self.original_stdout.flush()
        self.file.flush()
    
    def flush(self):
        self.original_stdout.flush()
        self.file.flush()

def start_server():    
    app = Application([
        (r"/ws/test/", PongBot)
    ], websocket_ping_interval=10, websocket_ping_timeout=30)
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()



def build_client():
    print(f"{BLUE}[BUILD] Building TypeScript client...{RESET}")

    load_dotenv()
    env = os.environ.copy()
    
    node_path = os.getenv("NODE_PATH")
    
    if node_path:
        node_path = node_path.strip().strip('"').strip("'")
        
        if os.name == 'nt':
            env["PATH"] = node_path + ";" + env["PATH"]
        else:
            env["PATH"] = node_path + "/bin:" + env["PATH"]

    with open(os.devnull, 'w') as devnull:
        if os.name == 'nt':
            result = subprocess.run(["npm", "install", "typescript"], cwd="client", 
                                    env=env, shell=True, stdout=devnull, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(result.stderr)
                return
            result = subprocess.run(["npx", "tsc"], cwd="client", 
                                    env=env, shell=True, stdout=devnull, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(result.stderr)
                return
        else:
            result = subprocess.run(["npm", "install", "typescript"], cwd="client", 
                                    env=env, stdout=devnull, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(result.stderr)
                return
            
            result = subprocess.run(["npx", "tsc"], cwd="client", 
                                    env=env, stdout=devnull, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(result.stderr)
                return
    
    print(f"{BLUE}[BUILD] TypeScript build completed{RESET}")


def run_client():
    timestamp = time.strftime('%H:%M:%S')
    
    process = subprocess.Popen(
        ["node", "client/dist/client.test.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            timestamp = time.strftime('%H:%M:%S')
            print(f"{BLUE}[CLIENT {timestamp}] {output.strip()}{RESET}")
    
    process.wait()


def test_client_server_exchange():   
    with open("output.txt", "w", encoding="utf-8") as output_file:
        original_stdout = sys.stdout
        sys.stdout = TeeOutput(output_file, original_stdout)
        
        thread = threading.Thread(target=start_server, daemon=True)
        thread.start()
        time.sleep(1)

        build_client()
        run_client()

        tornado.ioloop.IOLoop.current().stop()
        
        sys.stdout = original_stdout
        print("Output has been saved to output.txt")

    with open("output.txt", "r", encoding="utf-8") as output_file:
        output = output_file.read()
        
        lines = []
        for line in output.split('\n'):
            if line.strip():
                if 'CLIENT' in line:
                    lines.append({'content': line, 'type': 'client'})
                elif 'SERVER' in line:
                    lines.append({'content': line, 'type': 'server'})
                else:
                    lines.append({'content': line, 'type': 'other'})
        
        print("Lines in order:")
        for i, line in enumerate(lines):
            print(f"  {i+1}. [{line['type'].upper()}] {line['content']}")
        
        client_lines = [line['content'] for line in lines if line['type'] == 'client']
        server_lines = [line['content'] for line in lines if line['type'] == 'server']
        
        client_output = '\n'.join(client_lines)
        assert 'Client connected!' in client_output, "Client connection message not found"
        assert 'Received from server: {"move": -1, "start": 1}' in client_output, "Expected server response not found"
        
        server_output = '\n'.join(server_lines)
        assert 'WebSocket connection opened' in server_output, "Server connection message not found"
        assert 'Sending response: {"move": -1, "start": 1}' in server_output, "Server response message not found"
        
        print(f"\nFound {len(client_lines)} client lines and {len(server_lines)} server lines")
        print("All assertions passed!")


if __name__ == "__main__":
    test_client_server_exchange()
