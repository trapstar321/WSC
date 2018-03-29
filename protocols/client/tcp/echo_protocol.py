from protocols.client.tcp.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import json

logger = ConsoleLogger('protocols/client/tcp/echo_protocol.py')


class EchoProtocol(AckProtocol):
    def on_connected(self):
        super(EchoProtocol, self).on_connected()
        logger.info('Connected')
        #message = 'Hi\n'.encode('utf-8')
        #message = super(EchoProtocol, self).send(message)
        #self.client.send(message)

    def on_disconnected(self):
        super(EchoProtocol, self).on_disconnected()
        logger.info('Disconnected')

    def on_message(self, message):
        #call AckProtocol on_message so it removes ack in message
        message = json.loads(message.decode('utf-8'))
        message = super(EchoProtocol, self).on_message(message)

        if message:
            message['msg'] = 'Hi'
            logger.info('Received => {}'.format(message))

            #time.sleep(2)
            self.send(message)

    def send(self, message):
        #call AckProtocol send so it adds ack in message
        message = super(EchoProtocol, self).send(message)
        logger.info('Send => {}'.format(message))
        message = json.dumps(message).encode('utf-8')+'\n'.encode('utf-8')
        self.client.send(message)

