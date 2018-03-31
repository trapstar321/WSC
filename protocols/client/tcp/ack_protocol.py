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
        self.acks=[]
        self.lock = threading.Lock()
        self.msg_id_counter=0

    def gen_msg_id(self):
        with self.lock:
            if self.msg_id_counter==sys.maxsize:
                self.msg_id_counter=0
            self.msg_id_counter+=1
        return self.msg_id_counter

    def on_connected(self):
        #check if something on queue and return all messages ordered by id
        #if next server message is ack, doesn't matter will be sent twice

        message = super(AckProtocol, self).on_connected()
        self.send(message)

        for ack in self.acks:
            self.send(ack)

        #must ignore message with dev_id key
        msg_ids = list(self.queue.keys())

        def message_to_remove(msg_ids, key):
            for id_ in msg_ids:
                message = self.queue[id_]
                msg_keys = list(message.keys())
                if key in msg_keys:
                    return id_

        msg_ids.remove(message_to_remove(msg_ids, 'dev_id'))

        for id_ in msg_ids:
            message = self.queue[id_]
            message['resend'] = 1
            self.send(message)

        return message

    def on_disconnected(self):
        pass

    def on_message(self, message):
        super(AckProtocol, self).on_message(message)

        self.acks.clear()

        # acknowledge message
        if 'ack' in message:
            msg_id = message['ack']
            try:
                del self.queue[msg_id]
            except KeyError as e:
                logger.info('KeyError self.queue: {}'.format(str(e)))

            logger.info('Got ack for message {}'.format(message))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}
            self.acks.append(ack)

            logger.info('Return ack {} for message'.format(message))
            self.send(ack)

        return message

    def send(self, message):
        super(AckProtocol, self).send(message)
        # add message_id to message so it can be acknowledged, only if not ack message

        # add message_id to message so it can be acknowledged, only if not ack message
        if 'ack' not in message and 'resend' not in message:
            id_ = self.gen_msg_id()
            self.queue[id_] = message

            message['id'] = id_
            logger.info('Signed message {}'.format(message))

        if 'resend' in message:
            logger.info('Resend message {}'.format(message))
            del message['resend']

        return message
