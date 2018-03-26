from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer as TornadoTCPServer

import asyncio

class Protocol(object):
    def __init__(self):
        self.clients = {}

    def on_client_connected(self, address, stream):
        self.clients[address]=stream

    def on_client_disconnected(self, address):
        del self.clients[address]

    def on_message(self, address, message):
        pass

    def send(self, address, message):
        pass

class EchoProtocol(Protocol):
    def on_client_connected(self, address, stream):
        super(EchoProtocol,self).on_client_connected(address, stream)
        print('Client {} connected'.format(address))

    def on_client_disconnected(self, address):
        super(EchoProtocol, self).on_client_disconnected(address)
        print('Client {} disconnected'.format(address))

    def on_message(self, address, message):
        print('Got message {} from client {}'.format(message, address))
        self.send(self.clients[address], message)

    def send(self, stream, message):
        self.server.send(stream, message)

class TCPServer(TornadoTCPServer):
    """Tornado asynchronous echo TCP server."""

    def __init__(self, port, protocol):
        super(TCPServer, self).__init__()
        self.port=port
        self.protocol=protocol
        self.protocol.server=self

        self.loop = asyncio.get_event_loop()
        self.listen(port)

        IOLoop.instance().start()

    #client connected
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, fileno = address
        self.protocol.on_client_connected(address, stream)
        while True:
            try:
                data = yield stream.read_until('\n'.encode('utf-8'))
                self.protocol.on_message(address, data)
            except StreamClosedError:
                self.protocol.on_client_disconnected(address)
                break

    def send(self, stream, message):
        self.loop.call_soon_threadsafe(asyncio.async, self.write(stream, message))

    async def write(self, stream, message):
        await stream.write(message)


if __name__ == "__main__":
    protocol = EchoProtocol()
    server = TCPServer(8080, protocol)

