import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path

from tornado.options import define, options
from protocols.server.websocket.query_protocol import QueryProtocol
from utils.logging import ConsoleLogger
logger = ConsoleLogger('wsock_server.py')

import uuid, logging

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", WebSocketServer),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients={}
    protocol=None

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.address = self.stream.socket.getpeername()
        WebSocketServer.clients[self.address]=self
        WebSocketServer.protocol.on_connected(self.address)

    def on_close(self):
        del WebSocketServer.clients[self.address]
        WebSocketServer.protocol.on_disconnected(self.address)

    def on_message(self, message):
        WebSocketServer.protocol.on_message(self.stream.socket.getpeername(), message, self.request.headers)

    @classmethod
    def send(self, address, message):
        WebSocketServer.clients[address].write_message(message)

def main():
    tornado.options.parse_command_line()
    WebSocketServer.protocol = QueryProtocol()
    WebSocketServer.protocol.server = WebSocketServer
    app = Application()
    app.listen(options.port)

    #had some problems with double logging, here they are all disabled
    for key in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(key)
        lg.propagate=False

    logger.info('Listening on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()