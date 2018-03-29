from protocols.client.tcp.identity_protocol import IdentityProtocol
from utils.logging import ConsoleLogger
import threading
import sys
import json

logger = ConsoleLogger('protocols/client/tcp/ack_protocol.py')


class AckProtocol(IdentityProtocol):
    def __init__(self):
        super(AckProtocol, self).__init__()
        self.queue={}
        self.lock = threading.Lock()
        self.msg_id_counter=0

    def gen_msg_id(self):
        with self.lock:
            if self.msg_id_counter==sys.maxsize:
                self.msg_id_counter=0
            self.msg_id_counter+=1
        return self.msg_id_counter

    def on_message(self, message):
        message = super(AckProtocol, self).on_message(message)

        # acknowledge message
        if 'ack' in message:
            msg_id = message['ack']
            del self.queue[msg_id]

            logger.info('Got ack for message {}'.format(message))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}

            logger.info('Return ack {} for message'.format(message))
            self.send(ack)

        return message

    def send(self, message):
        super(AckProtocol, self).send(message)
        # add message_id to message so it can be acknowledged, only if not ack message

        # add message_id to message so it can be acknowledged, only if not ack message
        if 'ack' not in message:
            id_ = self.gen_msg_id()
            self.queue[id_] = message

            message['id'] = id_
            logger.info('Signed message {}'.format(message))

        return message
