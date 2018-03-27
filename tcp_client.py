from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient as TornadoTCPClient
from utils.logging import ConsoleLogger
import logging, time
from protocols.client.tcp.echo_protocol import  EchoProtocol

import asyncio, threading

logger = ConsoleLogger('tcp_client.py')

class TCPClient(object):
    def __init__(self, address, port, protocol):
        self.address = address
        self.port = port
        self.protocol=protocol
        self.protocol.client = self

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
        return not self.stream.closed()

    async def connect(self):
        self.stream = await TornadoTCPClient().connect(self.address, self.port)
        self.protocol.on_connected()

    def send(self, message):
        if self.stream.closed():
            raise Exception('Client not connected')
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