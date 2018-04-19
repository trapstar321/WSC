from protocols.server.websocket.identity_protocol import IdentityProtocol
from utils.logging import ConsoleLogger
import threading, sys
import json

logger = ConsoleLogger('protocols/server/websocket/ack_protocol.py')


class AckProtocol(IdentityProtocol):
    def __init__(self):
        super(AckProtocol, self).__init__()
        self.queue={}
        self.acks = {}
        self.address_id_map={}
        self.id_address_map={}

    def gen_msg_id(self, client_id):
        lock = self.queue[client_id]['lock']

        with lock:
            if self.queue[client_id]['msg_counter']==sys.maxsize:
                self.queue[client_id]['msg_counter']=0
            self.queue[client_id]['msg_counter']+=1
        return self.queue[client_id]['msg_counter']

    def reconnected(self, client_id, address):
        for ack in self.acks[client_id]:
            self.send(address, ack)

        queue = self.queue[client_id]['queue']
        keys = list(queue.keys())
        for key in keys:
            message = queue[key]
            message['resend'] = 1
            self.send(address, message)

    def id_from_address(self, address):
        return self.address_id_map[address]

    def address_from_id(self, id_):
        return self.id_address_map[id_]

    def on_connected(self, address):
        message = super(AckProtocol,self).on_connected(address)
        self.send(address, message)

    def on_message(self, address, message, headers):
        super(AckProtocol, self).on_message(address, message, headers)

        message['forward'] = 1

        if 'client_id' in message:
            # store client in queue and map
            id_ = message['client_id']

            found = id_ in self.queue
            #check if client_id already exists and address is different

            if found:
                for old_address in self.address_id_map:
                    #if address is different remap
                    old_id = self.address_id_map[old_address]
                    if old_id==id_ and old_address!=address:
                        logger.info('Remap client {} address old={}, new={}'.format(id_, old_address, address))
                        del self.address_id_map[old_address]
                        self.address_id_map[address]=id_
                        self.id_address_map[id_]=address
                        message['remap'] = 1
                        message['old_address'] = old_address
                        message['reconnected']=1
                        break
                message['forward']=0
            else:
                #client is making new connection, make new message queue
                logger.info('Make message queue for client={}, address={}'.format(id_, address))
                self.queue[id_] = {'lock': threading.Lock(), 'queue': {}, 'msg_counter': 0}
                self.acks[id_]=[]
                self.address_id_map[address] = id_
                self.id_address_map[id_]=address

                message['add_client']=id_
                message['forward'] = 0
                message['connected'] = 1

            logger.info('Process queue for client={}, address={}'.format(id_, address))
            self.reconnected(id_, address)
            #del message['client_id']

        id_ = self.address_id_map[address]

        #we can clear old acks because if client was reconnected, acks are resent
        self.acks[id_].clear()

        #acknowledge message
        if 'ack' in message:
            msg_id=message['ack']
            try:
                del self.queue[id_]['queue'][msg_id]
            except KeyError as e:
                logger.info('KeyError self.queue[{}]: {}'.format(id_, str(e)))

            logger.info('Got ack for message {} from client {}'.format(msg_id, address))
            return None
        else:
            # return ack and extract message
            msg_id = message['id']
            ack = {'ack': msg_id}
            self.acks[id_].append(ack)

            logger.info('Return ack {} for message {}'.format(ack, message))
            self.send(address, ack)

        return message

    def send(self, address, message):
        super(AckProtocol, self).send(address, message)
        if address in self.address_id_map:
            client_id = self.address_id_map[address]

            # add message_id to message so it can be acknowledged, only if not ack message
            if 'ack' not in message and 'resend' not in message:
                id_ = self.gen_msg_id(client_id)
                self.queue[client_id]['queue'][id_] = message

                message['id'] = id_
                logger.info('Signed message {} for client {}'.format(message, address))

            if 'resend' in message:
                logger.info('Resend message {} to client {}'.format(message, address))
                del message['resend']

        return message
