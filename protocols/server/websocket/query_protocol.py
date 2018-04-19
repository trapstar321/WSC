from protocols.server.websocket.browser_device_protocol import BrowserDeviceProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/server/websocket/query_protocol.py')

class QueryProtocol(BrowserDeviceProtocol):
    def on_message(self, address, message, headers):
        super(QueryProtocol, self).on_message(address, message, headers)

        if 'query' in message:
            logger.info('Received query message {} from {}'.format(message, address))