from protocols.server.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import threading, sys
import json

logger = ConsoleLogger('protocols/server/tcp/ack_protocol.py')


class AckProtocol(Protocol):
    def __init__(self):
        super(AckProtocol, self).__init__()
        self.queue={}
        self.acks = {}
        self.address_id_map={}

    def gen_msg_id(self, device_id):
        lock = self.queue[device_id]['lock']

        with lock:
            if self.queue[device_id]['msg_counter']==sys.maxsize:
                self.queue[device_id]['msg_counter']=0
            self.queue[device_id]['msg_counter']+=1
        return self.queue[device_id]['msg_counter']

    def reconnected(self, device_id, address):
        for ack in self.acks[device_id]:
            self.send(address, ack)

        queue = self.queue[device_id]['queue']
        keys = list(queue.keys())
        for key in keys:
            message = queue[key]
            message['resend'] = 1
            self.send(address, message)

    def device_id(self, address):
        return self.address_id_map[address]

    def on_connected(self, address):
        super(AckProtocol,self).on_connected(address)

    def on_disconnected(self, address):
        super(AckProtocol, self).on_connected(address)
        return self.address_id_map[address]

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
                self.acks[id_]=[]
                self.address_id_map[address] = id_

                message['add_device']=id_
                message['forward'] = 0

            logger.info('Process queue for device={}, address={}'.format(id_, address))
            self.reconnected(id_, address)
            del message['dev_id']

        id_ = self.address_id_map[address]

        #we can clear old acks because if device was reconnected, acks are resent
        self.acks[id_].clear()

        #acknowledge message
        if 'ack' in message:
            msg_id=message['ack']
            try:
                del self.queue[id_]['queue'][msg_id]
            except KeyError as e:
                logger.info('KeyError self.queue[{}]: {}'.format(id_, str(e)))

            logger.info('Got ack for message {} from client {}'.format(message, address))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}
            self.acks[id_].append(ack)

            logger.info('Return ack {} for message'.format(message))
            self.send(address, ack)

        return message

    def send(self, address, message):
        super(AckProtocol, self).send(address, message)
        device_id=self.address_id_map[address]

        # add message_id to message so it can be acknowledged, only if not ack message
        if 'ack' not in message and 'resend' not in message:
            id_ = self.gen_msg_id(device_id)
            self.queue[device_id]['queue'][id_] = message

            message['id'] = id_
            logger.info('Signed message {} for client {}'.format(message, address))

        if 'resend' in message:
            logger.info('Resend message {} to client {}'.format(message, address))
            del message['resend']

        return message
