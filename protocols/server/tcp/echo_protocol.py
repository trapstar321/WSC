from protocols.server.tcp.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/server/tcp/echo_protocol.py')


class EchoProtocol(AckProtocol):
    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)
        logger.info('Client {} connected'.format(address))

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)
        logger.info('Client {} disconnected'.format(address))

    def on_message(self, address, message):
        message = message.decode('utf-8')
        message = json.loads(message)
        message = super(EchoProtocol, self).on_message(address, message)

        if message:
            logger.info('Received message {} from client {}'.format(message, address))
            dev_id = super(EchoProtocol, self).device_id(address)
            if 'add_device' in message:
                server = self.server
                server.d_b_connector.add_device(server.websocketserver_id, dev_id, address)
                self.send(address, message)
            elif message['forward']==1:
                self.server.d_b_connector.on_device_message(dev_id, message)
            elif 'remap' in message:
                self.server.d_b_connector.address_changed(dev_id, message['new_address'])
                self.send(address, message)
            else:
                self.send(address, message)


    def send(self, address, message):
        message = super(EchoProtocol, self).send(address, message)
        if 'add_device' in message:
            del message['add_device']
        if 'forward' in message:
            del message['forward']
        if 'remap' in message:
            del message['remap']
        if 'new_address' in message:
            del message['new_address']

        logger.info('Send message {} to client {}'.format(message, address))
        message = json.dumps(message).encode('utf-8') + '\n'.encode('utf-8')
        self.server.send(address, message)
