from protocols.server.tcp.identity_protocol import IdentityProtocol
from utils.logging import ConsoleLogger
import threading, sys
import json

logger = ConsoleLogger('protocols/server/tcp/ack_protocol.py')


class AckProtocol(IdentityProtocol):
    def __init__(self):
        super(AckProtocol, self).__init__()
        self.queue={}
        self.address_id_map={}

    def gen_msg_id(self, client_id):
        lock = self.queue[client_id]['lock']

        with lock:
            if self.queue[client_id]['msg_counter']==sys.maxsize:
                self.queue[client_id]['msg_counter']=0
            self.queue[client_id]['msg_counter']+=1
        return self.queue[client_id]['msg_counter']

    def on_connected(self, address):
        id_ = super(AckProtocol,self).on_connected(address)
        #add lock and message counter for client
        self.queue[id_]={'lock': threading.Lock(), 'queue': {}, 'msg_counter': 0}
        self.address_id_map[address]=id_

        msg = {'client_id': id_}
        self.send(address, msg)

    def send(self, address, message):
        super(AckProtocol, self).send(address, message)
        client_id=self.address_id_map[address]


        # add message_id to message so it can be acknowledged, only if not ack message
        if 'ack' not in message:
            id_ = self.gen_msg_id(client_id)
            self.queue[client_id]['queue'][id_] = message

            message['id'] = id_
            logger.info('Signed message {} for client {}'.format(message, address))

        return message

    def on_message(self, address, message):
        super(AckProtocol, self).on_message(address, message)
        client_id=self.address_id_map[address]

        #acknowledge message
        if 'ack' in message:
            msg_id=message['ack']
            del self.queue[client_id]['queue'][msg_id]

            logger.info('Got ack for message {} from client {}'.format(message, address))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}

            logger.info('Return ack {} for message'.format(message))
            self.send(address, ack)

        return message
