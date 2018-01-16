"""Module with 2d location class."""
import math

class Location2D(object):
    """Defines location in 2D space."""

    def __init__(self, x=0.0, y=0.0):
        """2D location constructor."""
        self.position_x = x
        self.position_y = y

    def distance(self, other_location):
        """Calculates distance between this location and another 2d location."""
        return math.sqrt((self.position_x - other_location.position_x)**2 +
                         (self.position_y - other_location.position_y)**2)
