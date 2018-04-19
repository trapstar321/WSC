from protocols.client.websocket.query_protocol import QueryProtocol
from wsock_client import WebSocketClient

client = WebSocketClient("ws://{}:{}".format("127.0.0.1", "8888"), QueryProtocol(), 5, {'Query':'1'})
client.connect()