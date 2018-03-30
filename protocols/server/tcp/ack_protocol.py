from protocols.server.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import threading, sys
import json

logger = ConsoleLogger('protocols/server/tcp/ack_protocol.py')


class AckProtocol(Protocol):
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

    def device_id(self, address):
        return self.address_id_map[address]

    def on_connected(self, address):
        #identity protocol returns message with dev_id
        message = super(AckProtocol,self).on_connected(address)

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

        message['forward'] = 1

        if 'dev_id' in message:
            # store device in queue and map
            id_ = message['dev_id']

            found = id_ in self.queue
            #check if device_id already exists and address is different

            if found:
                for old_address in self.address_id_map:
                    #if address is different remap
                    old_id = self.address_id_map[old_address]
                    if old_id==id_ and old_address!=address:
                        logger.info('Remap device {} address old={}, new={}'.format(id_, old_address, address))
                        del self.address_id_map[old_address]
                        self.address_id_map[address]=id_
                        message['remap'] = 1
                        message['new_address'] = address
                        break
                message['forward']=0
            else:
                #device is making new connection, make new message queue
                logger.info('Make message queue for device={}, address={}'.format(id_, address))
                self.queue[id_] = {'lock': threading.Lock(), 'queue': {}, 'msg_counter': 0}
                self.address_id_map[address] = id_

                message['add_device']=id_
                message['forward'] = 0
            del message['dev_id']

        id_ = self.address_id_map[address]

        #acknowledge message
        if 'ack' in message:
            msg_id=message['ack']
            del self.queue[id_]['queue'][msg_id]

            logger.info('Got ack for message {} from client {}'.format(message, address))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}

            logger.info('Return ack {} for message'.format(message))
            self.send(address, ack)

        return message
