import math


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other_location):
        return math.sqrt((self.x - other_location.x)**2 + (self.y - other_location.y)**2)