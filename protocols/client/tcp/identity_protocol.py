from protocols.client.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/tcp/identity_protocol.py')


#return some ID to server on connect
class IdentityProtocol(Protocol):
    def on_connected(self):
        super(IdentityProtocol, self).on_connected()
        return {'dev_id': 1}

