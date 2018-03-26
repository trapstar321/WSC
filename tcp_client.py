from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient as TornadoTCPClient
import concurrent.futures

import asyncio, threading

class Protocol(object):
    def on_message(self, message):
        pass

    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def send(self, message):
        pass

class EchoProtocol(Protocol):
    def on_message(self, message):
        print('Recv: {}'.format(message))
        self.send('Hi\n')

    def on_connected(self):
        print('Connected')
        #self.client.send('Hi\n')

    def on_disconnected(self):
        print('Disconnected')

    def send(self, message):
        print('Send: {}'.format(message))
        self.client.send(message)

class TCPClient(object):
    def __init__(self, address, port, protocol):
        self.address = address
        self.port = port
        self.protocol=protocol
        self.protocol.client = self

        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.connect())

        t = threading.Thread(target=self.start, args=(self.loop,))
        t.start()

    def start(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.read())

    def send(self, message):
        self.loop.call_soon_threadsafe(asyncio.async, self.write(message))

    async def write(self, message):
        await self.stream.write(message.encode('utf-8'))

    async def read(self):
        try:
            while True:
                reply = await self.stream.read_until('\n'.encode('utf-8'))
                self.protocol.on_message(reply)
        except StreamClosedError as e:
            self.protocol.on_disconnected()

    async def connect(self):
        self.stream = await TornadoTCPClient().connect(self.address, self.port)
        self.protocol.on_connected()

if __name__=="__main__":
    print("Starting client...")
    protocol = EchoProtocol()
    client = TCPClient('127.0.0.1', 8080, protocol)

    import time
    #time.sleep(0.5)
    protocol.send('Hi\n')
    time.sleep(20)