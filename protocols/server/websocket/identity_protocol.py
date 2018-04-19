from protocols.server.websocket.protocol import Protocol
from utils.logging import ConsoleLogger
import threading, sys
import json
from threading import Lock

logger = ConsoleLogger('protocols/server/websocket/identity_protocol.py')

class IdentityProtocol(Protocol):
    client_id_counter=0
    lock = Lock()

    def gen_client_id(self):
        id_ = 0
        IdentityProtocol.lock.acquire()
        IdentityProtocol.client_id_counter+=1
        id_= IdentityProtocol.client_id_counter
        IdentityProtocol.lock.release()
        return id_

    def on_connected(self, address):
        super(IdentityProtocol, self).on_connected(address)
        return {'unique_client_id':self.gen_client_id()}

    def on_disconnected(self, address):
        super(IdentityProtocol, self).on_disconnected(address)

    def on_message(self, address, message, headers):
        super(IdentityProtocol, self).on_message(address, message, headers)

    def send(self, address, message):
        super(IdentityProtocol, self).send(address, message)