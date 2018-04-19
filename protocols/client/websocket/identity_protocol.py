from protocols.client.websocket.protocol import Protocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/websocket/identity_protocol.py')


#return some ID to server on connect
class IdentityProtocol(Protocol):
    def __init__(self):
        self.client_id=None

    def on_message(self, message):
        if 'unique_client_id' in message:
            if not self.client_id:
                self.client_id=message['unique_client_id']
            return {'client_id':self.client_id}
        return None


