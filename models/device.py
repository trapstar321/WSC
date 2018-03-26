class Device(object):
    def __init__(self, socket_handler, id, address):
        self.socket_handler = socket_handler
        self.id=id
        self.address=address