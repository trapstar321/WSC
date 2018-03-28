from protocols.client.websocket.protocol import Protocol
from utils.logging import ConsoleLogger

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
        return "({})".format(device_id)+message

    # connector will call extract label after receiving message
    def extract_label(self, message):
        start = message.index('(')
        end = message.index(')')
        return message[start+1:end]

    def extract_message(self, message):
        end = message.index(')')
        return message[end+1:]