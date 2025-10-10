import tornado.ioloop
from tornado.web import Application

from src.game import PongWebSocketHandler


def start_server():
    app = Application([
        (r"/ws/test/", PongWebSocketHandler)
    ])
    app.listen(8000)

    print("Server is listening on port 8000")

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_server()