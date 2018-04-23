from protocols.client.tcp.ack_protocol import AckProtocol
from utils.logging import ConsoleLogger
import json
import asyncio
import random

logger = ConsoleLogger('protocols/client/tcp/weather_station_protocol.py')


class WeatherStationProtocol(AckProtocol):
    @asyncio.coroutine
    def send_weather_data(self):
        yield from asyncio.sleep(4)
        message={'temperature':random.randint(0,30), 'humidity':random.randint(0,100)}
        self.send(message)

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.send_weather_data())
        return True

    def on_connected(self):
        super(WeatherStationProtocol, self).on_connected()
        logger.info('Connected')

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.send_weather_data())
        #loop.run_until_complete(task)

    def on_disconnected(self):
        super(WeatherStationProtocol, self).on_disconnected()
        logger.info('Disconnected')

    def on_message(self, message):
        #call AckProtocol on_message so it removes ack in message
        message = json.loads(message.decode('utf-8'))
        message = super(WeatherStationProtocol, self).on_message(message)

        # TODO: if needs to respond to message, do it here

    def send(self, message):
        #call AckProtocol send so it adds ack in message
        message = super(WeatherStationProtocol, self).send(message)
        logger.info('Send => {}'.format(message))
        message = json.dumps(message).encode('utf-8')+'\n'.encode('utf-8')
        self.client.send(message)

