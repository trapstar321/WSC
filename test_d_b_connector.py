from dev_brows_connector import DeviceBrowserConnector
from protocols.server.tcp.echo_protocol import EchoProtocol

d_b_connector = DeviceBrowserConnector(EchoProtocol())
server_id = d_b_connector.add_server('127.0.0.1', 8888)

device1=("127.0.0.1", 1234)
device2=("127.0.0.1", 1235)

d_b_connector.add_device(server_id, device1)
d_b_connector.add_device(server_id, device2)

#TEST 1 remove server, all devices connected to server should be removed also
#d_b_connector.remove_server(server_id)

#TEST 2 remove device, device should be removed from server
d_b_connector.remove_device(device1)
s = ""