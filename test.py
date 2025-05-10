import os
import subprocess
import threading

import tornado.ioloop
from dotenv import load_dotenv
from tornado.web import Application

from server.game import PongBot


def start_server():
    app = Application([
        (r"/ws/test/", PongBot)
    ], websocket_ping_interval=10, websocket_ping_timeout=30)
    app.listen(8000)
    
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        tornado.ioloop.IOLoop.current().stop()


def build_client():
    print("Building TypeScript client...")
    load_dotenv()
    env = os.environ.copy()
    env["PATH"] = os.getenv("NODE_PATH") + "/bin:" + env["PATH"]

    subprocess.run(["npm", "install", "typescript"], cwd="client", check=True, env=env)
    subprocess.run(["npx", "tsc"], cwd="client", check=True, env=env)


def test_client_server_exchange():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

    build_client()
    result = subprocess.run(
        ["node", "client/dist/client.test.js"],
        capture_output=True,
        text=True,
        timeout=50
    )

    tornado.ioloop.IOLoop.current().stop()

    client_output = result.stdout

    assert 'Client connected!' in client_output
    assert 'Received from server: {"move": 1, "start": 1}' in client_output


if __name__ == "__main__":
    test_client_server_exchange()
