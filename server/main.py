import tornado.ioloop
from tornado.web import Application

from server.src.game import PongBot


def start_server():    
    app = Application([
        (r"/ws/test/", PongBot)
    ], websocket_ping_interval=10, websocket_ping_timeout=30)
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()

def stop_server():
    tornado.ioloop.IOLoop.current().stop()