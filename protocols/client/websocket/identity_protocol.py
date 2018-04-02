from protocols.client.websocket.protocol import Protocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/websocket/identity_protocol.py')


#return some ID to server on connect
class IdentityProtocol(Protocol):
    def on_connected(self):
        super(IdentityProtocol, self).on_connected()
        return {'client_id': 1}

