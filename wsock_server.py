import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path

from tornado.options import define, options

from models.browser import Browser
from models.device import Device

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
    browsers={}
    devices={}

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        address = self.stream.socket.getpeername()
        if 'User-Agent' in self.request.headers:
            logger.info('Add browser. Address={}'.format(str(address)))
            WebSocketServer.browsers[self]=Browser(self, self.request.headers['User-Agent'], address)
        else:
            logger.info('Add device. Address={}'.format(str(address)))
            WebSocketServer.devices[self] = Device(self, str(uuid.uuid1()), address)

    def on_close(self):
        # TODO: if device disconnects notify browsers
        if self in WebSocketServer.devices:
            logger.info('Remove device. Address={}'.format(str(WebSocketServer.devices[self].address)))
            del WebSocketServer.devices[self]
        else:
            logger.info('Remove browser. Address={}'.format(str(WebSocketServer.browsers[self].address)))
            del WebSocketServer.browsers[self]

    def on_message(self, message):
        logger.info('Received => {}'.format(message))
        self.write_message(message)

def main():
    tornado.options.parse_command_line()
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