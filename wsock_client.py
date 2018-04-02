from tornado.websocket import websocket_connect, WebSocketClosedError
from tornado.iostream import StreamClosedError
from utils.logging import ConsoleLogger
import time
import asyncio, threading

logger = ConsoleLogger('wsock_client.py')

class WebSocketClient(object):
    def __init__(self, url, protocol, timeout):
        self.url = url
        self.protocol = protocol;
        self.protocol.client=self
        self.timeout = timeout
        self.loop = None
        self.client = None

    def connect(self):
        try:
            logger.info('Connecting...')
            self.loop = asyncio.new_event_loop()
            self.loop.run_until_complete(self.connect_())

            self.t = threading.Thread(target=self.start, args=(self.loop,))
            self.t.start()
        except StreamClosedError as e:
            self.protocol.on_disconnected()

    def disconnect(self):
        try:
            self.client.stream.close()
        except RuntimeError as e:
            logger.info('Runtime error: {}'.format(str(e)))

        self.loop.stop()
        while self.loop.is_running():
            time.sleep(0.2)
        self.loop.close()

        logger.info('Disconnect end')

    def start(self, loop):
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.read())
        except RuntimeError as e:
            logger.info('Runtime error: {}'.format(str(e)))

    def connected(self):
        return not self.client.stream.closed()

    async def connect_(self):
        self.client = await websocket_connect(self.url)
        self.protocol.on_connected()

    def send(self, message):
        if self.client.stream.closed():
            return False
        self.loop.call_soon_threadsafe(asyncio.async, self.write(message))

    async def write(self, message):
        try:
            await self.client.write_message(message)
        except WebSocketClosedError as e:
            self.protocol.on_disconnected()

    async def read(self):
        try:
            while True:
                reply = await self.client.read_message()
                if reply is None:
                    self.protocol.on_disconnected()
                    break
                self.protocol.on_message(reply)
        except WebSocketClosedError as e:
            self.protocol.on_disconnected()

    def keep_alive(self):
        if self.client.stream is None:
            self.connect()
        else:
            self.client.write_message("keep alive")

#if __name__ == "__main__":
    # had some problems with double logging, here they are all disabled
    #for key in logging.Logger.manager.loggerDict.keys():
    #    lg = logging.getLogger(key)
    #    lg.propagate=False

    #client = WebSocketClient("ws://localhost:8888", EchoProtocol(), 5)