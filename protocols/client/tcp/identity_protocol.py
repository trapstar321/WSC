from protocols.client.tcp.ack_protocol import Protocol
from utils.logging import ConsoleLogger
import time

logger = ConsoleLogger('protocols/client/tcp/echo_protocol.py')

#store id returned from server
class IdentityProtocol(Protocol):

    def on_message(self, message):
        super(IdentityProtocol, self).on_message(message)

        if '{client_id' in message.decode('utf-8'):
            #store client_id
            pass