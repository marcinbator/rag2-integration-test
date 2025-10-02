import tornado.ioloop
from tornado.web import Application

from src.game import PongBot


def start_server():    
    print("Server starting on port 8000...")
    app = Application([
        (r"/ws/test/", PongBot)
    ], websocket_ping_interval=10, websocket_ping_timeout=30)
    app.listen(8000)
    print("Server is listening on port 8000")

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_server()