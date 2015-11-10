class Message:
    """A message to be passed around the network"""

    def __init__(self, id, source, destination):
        self.id = id
        self.source = source
        self.destination = destination
        self.delivered = False
