from protocols.client.websocket.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import threading
import sys
import json

logger = ConsoleLogger('protocols/client/websocket/query_protocol.py')

class QueryProtocol(AckProtocol):
    def on_connected(self):
        super(QueryProtocol, self).on_connected()
        #message = {'query':1, 'params':{'dev_list':''}}
        #self.send(message)

    def on_message(self, message):
        super(QueryProtocol, self).on_message(message)