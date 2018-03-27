from protocols.client.websocket.message_labeling_protocol import MessageLabelingProtocol
from wsock_client import WebSocketClient

from utils.logging import ConsoleLogger

logger = ConsoleLogger('dev_browser_connector.py')

class Connection(object):
    def __init__(self, ip, address, protocol):
        self.ip=ip
        self.address=address

        self.protocol = protocol

    def connect(self):
        self.client = WebSocketClient("ws://{}:{}".format(self.ip, self.address), self.protocol, 5)

class DeviceBrowserConnector(object):
    def __init__(self, tcp_server_protocol):
        self.connections={}
        self.devices={}
        self.tcp_server_protocol = tcp_server_protocol
        self.protocol = MessageLabelingProtocol()

    #add new websocket server and connect
    def add_server(self, ip, port):
        logger.info('Add server ({},{})'.format(ip, port))
        protocol = MessageLabelingProtocol()
        # add connector to protocol so we can receive message in on_browser_message
        protocol.connector = self

        c = Connection(ip, port, protocol)
        c.connect()
        id_=id(c)
        logger.info('New server id={}'.format(id_))
        self.connections[id_]=c
        return id(c)

    #add device (address tuple) to server
    def add_device(self, server_id, device):
        logger.info('Add device {} to server {}'.format(device, server_id))
        self.devices[id(device)]={'server':server_id, 'address':device}

    # TODO: add disconnect method on client
    def remove_server(self, server_id):
        pass

    def remove_device(self, protocol):
        del self.devices[id(protocol)]

    #message from device, called from tcp server protocol
    def on_device_message(self, device, message):
        logger.info('Received message {} from device {}'.format(message, device))
        connection = self.connections[self.devices[id(device)]['server']]
        connection.protocol.send(self.protocol.label_message(id(device), message))

    #message from browser, called from protocol of connection
    def on_browser_message(self, message):
        logger.info('Received message {} from browser'.format(message))
        device_id =self.protocol.extract_label(message)
        address = self.devices[int(device_id)]['address']
        self.tcp_server_protocol.send(address, self.protocol.extract_message(message).encode('utf-8'))
