class Browser(object):
    def __init__(self, socket_handler, user_agent, address):
        self.socket_handler = socket_handler
        self.user_agent=user_agent
        self.address=address