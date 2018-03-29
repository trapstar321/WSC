from protocols.server.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import threading,sys

logger = ConsoleLogger('protocols/server/tcp/identity_protocol.py')

#just for generating client id's
class IdentityProtocol(Protocol):
    def __init__(self):
        super(IdentityProtocol, self).__init__()
        self.lock = threading.Lock()
        self.client_id_counter = 0

    def gen_client_id(self):
        with self.lock:
            if self.client_id_counter == sys.maxsize:
                self.client_id_counter = 0
            self.client_id_counter += 1
        return self.client_id_counter

    def on_connected(self, address):
        super(IdentityProtocol,self).on_connected(address)
        return self.gen_client_id()