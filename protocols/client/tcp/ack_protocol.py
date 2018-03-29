from protocols.client.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import threading, sys

logger = ConsoleLogger('protocols/client/tcp/ack_protocol.py')

class AckProtocol(Protocol):
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



    def send(self, message):
        super(AckProtocol, self).send(message)
        # add message_id to message so it can be acknowledged, only if not ack message
        if '{ack' not in message.decode('utf-8'):
            id_ = self.gen_msg_id()
            self.queue[id_] = message
            sign = '{id=' + str(id_) + '}'
            sign = sign.encode('utf-8')
            message = sign + message
            logger.info('Signed message {}'.format(message))

        return message


    def on_message(self, message):
        super(AckProtocol, self).on_message(message)
        rep = message.decode('utf-8')

        #acknowledge message
        if '{ack=' in rep:
            s = 5
            e = rep.index('}')
            msg_id = rep[s:e]
            del self.queue[int(msg_id)]

            logger.info('Got ack for message {}'.format(message))
            return None
        else:
            # return ack and extract message
            s = rep.index('{id=') + 4
            e = rep.index('}')
            msg_id = rep[s:e]
            ack = '{ack=' + msg_id + '}\n'

            logger.info('Return ack {} for message'.format(message))
            self.send(ack.encode('utf-8'))

            return rep[e + 1:].encode('utf-8')
