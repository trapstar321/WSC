from protocols.client.websocket.protocol import Protocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/websocket/message_labeling_protocol.py')


class MessageLabelingProtocol(Protocol):
    def on_connected(self):
        super(MessageLabelingProtocol, self).on_connected()
        logger.info('Connected')

    def on_disconnected(self):
        super(MessageLabelingProtocol,self).on_disconnected()
        logger.info('Disconnected')

    def on_message(self, message):
        super(MessageLabelingProtocol, self).on_message(message)
        logger.info('Received => {}'.format(message))
        self.connector.on_browser_message(message)

    def send(self, message):
        super(MessageLabelingProtocol, self).send(message)
        logger.info('Send => {}'.format(message))
        self.client.send(message)

    # connector will call label message before calling send
    def label_message(self, device_id, message):
        message['dev_id']=device_id
        return message

    # connector will call extract label after receiving message
    def extract_label(self, message):
        return message['dev_id']

