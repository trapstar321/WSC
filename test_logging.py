import logging
from utils.logging import ConsoleLogger



logger = ConsoleLogger('Test')

for key in logging.Logger.manager.loggerDict.keys():
    print(key)

logger = logging.getLogger('Test')
logger.propagate = False

logger.info('Test')

