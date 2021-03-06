from protocols.client.websocket.ack_protocol import AckProtocol
from wsock_client import WebSocketClient
import threading
from utils.logging import ConsoleLogger
import time

logger = ConsoleLogger('dev_browser_connector.py')


class Connection(object):
    def __init__(self, ip, address, protocol):
        self.ip=ip
        self.address = address
        self.protocol = protocol
        self.client = None

    def connect(self):
        self.client = WebSocketClient("ws://{}:{}".format(self.ip, self.address), self.protocol, 5)
        self.client.connect()

class DeviceBrowserConnector(object):
    def __init__(self, tcp_server_protocol):
        #connections are websocket servers
        self.connections={}
        #device are clients
        self.devices={}
        self.tcp_server_protocol = tcp_server_protocol

    #add new websocket server and connect
    def add_server(self, ip, port):
        logger.info('Add server ({},{})'.format(ip, port))
        protocol = AckProtocol()
        # add connector to protocol so we can receive message in on_browser_message
        protocol.connector = self

        c = Connection(ip, port, protocol)
        c.connect()
        id_=id(c)
        logger.info('New server id={}'.format(id_))
        self.connections[id_]=c
        return id(c)

    #add device (address tuple) to server
    def add_device(self, server_id, device, address):
        logger.info('Add device {} to server {}'.format(device, server_id))
        self.devices[device]={'server':server_id, 'address':address}

    # TODOD disconnect wsock_client if connected
    def remove_server(self, server_id):
        del self.connections[server_id]

        to_del = []

        for device_id in self.devices:
            srv_id=self.devices[device_id]['server']
            if server_id==srv_id:
                to_del.append(device_id)

        for key in to_del:
            del self.devices[key]

    def remove_device(self, device):
        logger.info('Remove device {}'.format(device))
        del self.devices[device]

    def address_changed(self, device, address):
        self.devices[device]['address']=address

    #message from device, called from tcp server protocol
    def on_device_message(self, device, message):
        logger.info('Received message {} from device {}'.format(message, device))
        connection = self.connections[self.devices[device]['server']]
        message['dev_id']=device
        connection.protocol.send(message)

    #message from browser, called from protocol of connection
    def on_browser_message(self, message):
        logger.info('Received message {} from browser'.format(message))
        device_id = message['dev_id']
        address = self.devices[device_id]['address']
        del message['dev_id']
        self.tcp_server_protocol.send(address, message)
