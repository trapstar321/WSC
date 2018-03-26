from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
from utils.logging import ConsoleLogger
import logging, time

logger = ConsoleLogger('wsock_client.py')

class Protocol(object):
    def _attach_ws(self, ws):
        self.ws = ws

    def on_message(self, message):
        logger.info('Received => {}'.format(message))

    def on_connected(self):
        logger.info('Connected')

    def on_close(self):
        logger.info('Disconnected')

    def write(self, message):
        self.ws.write_message(message)

class EchoProtocol(Protocol):
    def on_connected(self):
        self.write('Hi')

    def on_message(self, message):
        super(EchoProtocol, self).on_message(message)
        self.write(message)
        time.sleep(1)

class WebSocketClient(object):
    def __init__(self, url, protocol, timeout):
        self.url = url
        self.protocol = protocol;
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        #PeriodicCallback(self.keep_alive, 20000, io_loop=self.ioloop).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        logger.info("Trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
            self.protocol._attach_ws(self.ws)
        except Exception as e:
            logger.log_exception()
            self.ioloop.stop()
            self.protocol.on_close()
        else:
            logger.info("Connected")
            self.protocol.on_connected()
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                self.protocol.on_close()
                self.ws = None
                break
            else:
                self.protocol.on_message(msg)

        self.ioloop.stop()

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

if __name__ == "__main__":
    # had some problems with double logging, here they are all disabled
    for key in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(key)
        lg.propagate=False

    client = WebSocketClient("ws://localhost:8888", EchoProtocol(), 5)