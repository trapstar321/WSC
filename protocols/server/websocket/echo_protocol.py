from protocols.server.websocket.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/server/websocket/echo_protocol.py')


class EchoProtocol(AckProtocol):
    def __init__(self):
        super(EchoProtocol, self).__init__()
        # key is client_id, value is list of all device from that client
        # address can be obtained from address_id_map on AckProtocol
        self.dev_forwarder={}

        # key is client_id, value is the device the browser is currently viewing
        # address can be obtained from address_id_map on AckProtocol
        self.browsers={}

        #key is dev_id, value is a list of browsers (client_id) that are viewing the device
        self.browser_device_map={}

    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)
        logger.info('Client {} connected'.format(address))

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)
        logger.info('Client {} disconnected'.format(address))

    def on_message(self, address, message, headers):
        message = json.loads(message)
        message = super(EchoProtocol, self).on_message(address, message, headers)

        if message:
            logger.info('Received message {} from client {}'.format(message, address))
            if message['forward']:
                if 'connected' in message:
                    dev = message['dev_id']
                    logger.info('Notification: device {} connected'.format(dev))
                    self.add_device(address, dev)
                    self.broadcast_device_message(dev, message)
                elif 'disconnected' in message:
                    dev = message['dev_id']
                    logger.info('Notification: device {} disconnected'.format(dev))
                    self.broadcast_device_message(dev, message)
                elif 'choose' in message:
                    dev = message['dev_id']
                    message = self.choose_device(address, dev)
                    self.send(address, message)
                else:
                    dev = message['dev_id']
                    self.broadcast_device_message(dev, message)

            else:
                self.handle_connection(address, message, headers)

    def send(self, address, message):
        message = super(EchoProtocol, self).send(address, message)

        if 'client_id' in message:
            del message['client_id']
        if 'add_device' in message:
            del message['add_device']
        if 'forward' in message:
            del message['forward']
        if 'remap' in message:
            del message['remap']
        if 'new_address' in message:
            del message['new_address']

        logger.info('Send message {} to client {}'.format(message, address))
        message = json.dumps(message).encode('utf-8') + '\n'.encode('utf-8')
        self.server.send(address, message)

    def handle_connection(self, address, message, headers):
        if 'User-Agent' in headers:
            if 'connected' in message:
                logger.info('Browser client_id={}, address={} connected.'.format(message['client_id'], address))
                self.browsers[message['client_id']]=None
            elif 'reconnected' in message:
                logger.info('Browser client_id={}, old_address={}, new_address={} reconnected.'.format(message['client_id'],message['old_address'], address))
        else:
            if 'connected' in message:
                logger.info('Device message forwarder client_id={}, address={} connected.'.format(message['client_id'], address))
                self.dev_forwarder[message['client_id']]=[]
            elif 'reconnected' in message:
                logger.info('Device message forwarder client_id={}, old_address={}, new_address={} reconnected.'.format(message['client_id'],message['old_address'], address))

    #when device connects to tcp server, link it with websocket client on tcp server
    def add_device(self, address, dev):
        client_id = self.address_id_map[address]
        dev_list = self.dev_forwarder[client_id]
        if not dev in dev_list:
            logger.info('Add device {} to device list of client_id={}, address={}'.format(dev, client_id, address))
            dev_list.append(dev)

    #when browser chooses the device its viewing
    def choose_device(self, address, dev):
        client_id = self.address_id_map[address]

        # we can link browser with device even if its not connected
        self.browsers[client_id] = dev
        self.update_browser_device_link(dev, client_id)

        found = False
        for key in self.dev_forwarder:
            if found:
                break
            for device in self.dev_forwarder[key]:
                if device==dev:
                    found = True
                    break

        if found:
            logger.info('Browser client_id={}, address={} chose device {}. Device is connected!'.format(client_id, address,dev))
            return {'dev_id': dev, 'connected': 1}
        else:
            logger.info('Browser client_id={}, address={} chose device {}. Device is not connected!'.format(client_id, address,dev))
            return {'dev_id':dev, 'not_connected':1}

    def update_browser_device_link(self, dev, client_id):
        if dev not in self.browser_device_map:
            logger.info('Init browser_device_map for device {}'.format(dev))
            self.browser_device_map[dev]=[]

        if client_id not in self.browser_device_map[dev]:
            logger.info('Add client_id={} to browser_device_map for device {}'.format(client_id, dev))
            self.browser_device_map[dev].append(client_id)

    # these 2 method below will be slow, fix so a link between client_id and address exists
    def get_address(self, client_id):
        for address, id_ in self.address_id_map.items():
            if client_id == id_:
                return address

    def broadcast_device_message(self, dev, message):
        logger.info('Broadcast message {}.'.format(message))
        for client in self.browser_device_map[dev]:
            address = self.get_address(client)
            logger.info('Broadcast message {} from device {} to client_id={}, address={}'.format(message, dev, client, address))
            self.send(address, message)

