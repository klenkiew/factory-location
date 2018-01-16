"""Module with resource class."""


class Resource(object):
    """Class describing resource needed by factory."""

    def __init__(self, location, unit_transport_cost_function):
        self.location = location
        self.unit_transport_cost_function = unit_transport_cost_function


class ResourceRequirement:
    """Class which represents how many units of a given resource a factory needs"""
    def __init__(self, resource, required_units):
        self.resource = resource
        self.required_units = required_units