"""Module with factory class."""

class Factory(object):
    """Class describing factory."""

    def __init__(self, location, required_resources):
        self.location = location
        self.required_resources = required_resources
