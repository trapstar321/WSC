from protocols.server.websocket.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/server/websocket/echo_protocol.py')


class EchoProtocol(AckProtocol):
    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)
        logger.info('Client {} connected'.format(address))

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)
        logger.info('Client {} disconnected'.format(address))

    def on_message(self, address, message):
        message = json.loads(message)
        message = super(EchoProtocol, self).on_message(address, message)

        if message:
            logger.info('Received message {} from client {}'.format(message, address))
            if message['forward']:
                if 'connected' in message:
                    logger.info('Notification: device {} connected'.format(str(message['dev_id'])))
                elif 'disconnected' in message:
                    logger.info('Notification: device {} disconnected'.format(str(message['dev_id'])))
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
