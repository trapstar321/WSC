from protocols.client.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/tcp/identity_protocol.py')


#store id returned from server
class IdentityProtocol(Protocol):
    def __init__(self):
        self.client_id=None

    def on_message(self, message):
        super(IdentityProtocol, self).on_message(message)

        if 'client_id' in message:
            self.client_id = message['client_id']
            logger.info('Client_id={}'.format(self.client_id))
            del message['client_id']

        return message

