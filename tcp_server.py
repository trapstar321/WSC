from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer as TornadoTCPServer
from protocols.server.tcp.echo_protocol import EchoProtocol
from dev_brows_connector import DeviceBrowserConnector

import asyncio, logging

from utils.logging import ConsoleLogger
logger = ConsoleLogger('tcp_server.py')

class TCPServer(TornadoTCPServer):
    """Tornado asynchronous echo TCP server."""
    clients = {}

    def __init__(self, port, protocol):
        super(TCPServer, self).__init__()
        self.port=port
        self.protocol=protocol
        self.protocol.server=self

        self.loop = asyncio.get_event_loop()
        self.listen(port)

        logger.info('Listenining on port {}'.format(port))

        self.d_b_connector = DeviceBrowserConnector(self.protocol)
        self.websocketserver_id = self.d_b_connector.add_server('127.0.0.1', 8888)

        IOLoop.instance().start()

    #client connected
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, fileno = address
        TCPServer.clients[address]=stream
        self.protocol.on_connected(address)
        self.d_b_connector.add_device(self.websocketserver_id, address)
        while True:
            try:
                data = yield stream.read_until('\n'.encode('utf-8'))
                self.protocol.on_message(address, data)
            except StreamClosedError:
                del TCPServer.clients[address]
                self.protocol.on_disconnected(address)
                break

    def send(self, address, message):
        stream = TCPServer.clients[address]
        if stream.closed():
            raise Exception('Client not connected')
        self.loop.call_soon_threadsafe(asyncio.async, self.write(stream, message))

    async def write(self, stream, message):
        await stream.write(message)


if __name__ == "__main__":
    #had some problems with double logging, here they are all disabled
    for key in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(key)
        lg.propagate=False

    protocol = EchoProtocol()
    server = TCPServer(8080, protocol)

