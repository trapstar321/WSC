from tornado.websocket import websocket_connect, WebSocketClosedError
from tornado.iostream import StreamClosedError
from utils.logging import ConsoleLogger
import logging, time
import asyncio, threading
from protocols.client.websocket.echo_protocol import EchoProtocol

logger = ConsoleLogger('wsock_client.py')

class WebSocketClient(object):
    def __init__(self, url, protocol, timeout):
        self.url = url
        self.protocol = protocol;
        self.protocol.client=self
        self.timeout = timeout

        try:
            logger.info('Connecting...')
            self.loop = asyncio.new_event_loop()
            self.loop.run_until_complete(self.connect())

            t = threading.Thread(target=self.start, args=(self.loop,))
            t.start()
        except StreamClosedError as e:
            self.protocol.on_disconnected()

    def start(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.read())

    def connected(self):
        return not self.stream.stream.closed()

    async def connect(self):
        self.stream = await websocket_connect(self.url)
        self.protocol.on_connected()

    def send(self, message):
        if self.stream.stream.closed():
            raise Exception('Client not connected')
        self.loop.call_soon_threadsafe(asyncio.async, self.write(message))

    async def write(self, message):
        try:
            await self.stream.write_message(message)
        except WebSocketClosedError as e:
            self.protocol.on_disconnected

    async def read(self):
        try:
            while True:
                reply = await self.stream.read_message()
                if reply is None:
                    self.protocol.on_disconnected()
                    break
                self.protocol.on_message(reply)
        except WebSocketClosedError as e:
            self.protocol.on_disconnected()

    def keep_alive(self):
        if self.stream is None:
            self.connect()
        else:
            self.stream.write_message("keep alive")

if __name__ == "__main__":
    # had some problems with double logging, here they are all disabled
    for key in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(key)
        lg.propagate=False

    client = WebSocketClient("ws://localhost:8888", EchoProtocol(), 5)