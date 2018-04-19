from protocols.server.websocket.browser_device_protocol import BrowserDeviceProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/server/websocket/query_protocol.py')

class QueryProtocol(BrowserDeviceProtocol):
    def on_message(self, address, message, headers):
        message = json.loads(message)
        super(QueryProtocol, self).on_message(address, message, headers)

        if 'query' in message:
            client_id = self.address_id_map[address]
            params = message['params']
            logger.info('Got query with params={} from client_id={}, address={}'.format(params, client_id, address))

            if 'dev_list' in params:
                logger.info('Return device list to client_id={}, address={}'.format(client_id, address))
                result = []
                for dev, data in self.dev_status.items():
                    result.append({'dev': dev, 'connected': data['connected'], 'address': data['address']})
                message = {'dev_list':result}
                self.send(address, message)
