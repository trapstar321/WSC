from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient as TornadoTCPClient
from utils.logging import ConsoleLogger
import logging
from protocols.client.tcp.echo_protocol import  EchoProtocol
import time

import asyncio, threading

logger = ConsoleLogger('tcp_client.py')

class TCPClient(object):
    def __init__(self, address, port, protocol):
        self.address = address
        self.port = port
        self.protocol=protocol
        self.protocol.client = self
        self.loop = None

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
        self.loop.stop()
        while self.loop.is_running():
            time.sleep(0.2)
        self.loop.close()
        try:
            self.stream.close()
        except RuntimeError as e:
            logger.info('Runtime error: {}'.format(str(e)))
        logger.info('Disconnect end')


    def start(self, loop):
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.read())
        except RuntimeError as e:
            logger.info('Runtime error: {}'.format(str(e)))

    def connected(self):
        return not self.stream.closed()

    async def connect_(self):
        self.stream = await TornadoTCPClient().connect(self.address, self.port)
        self.protocol.on_connected()

    def send(self, message):
        if self.stream.closed():
            return False
        self.loop.call_soon_threadsafe(asyncio.async, self.write(message))

    async def write(self, message):
        try:
            await self.stream.write(message)
        except StreamClosedError as e:
            self.protocol.on_disconnected()

    async def read(self):
        try:
            while True:
                reply = await self.stream.read_until('\n'.encode('utf-8'))
                self.protocol.on_message(reply)
        except StreamClosedError as e:
            self.protocol.on_disconnected()

if __name__=="__main__":
    # had some problems with double logging, here they are all disabled
    for key in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(key)
        lg.propagate = False

    protocol = EchoProtocol()
    client = TCPClient('127.0.0.1', 8080, protocol)
    client.connect()


