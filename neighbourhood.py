"""Module with neighbourhood creation functions."""
import numpy
from location import Location2D


class Constraints:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.max_y = max_y
        self.min_y = min_y
        self.max_x = max_x
        self.min_x = min_x


def create_gaussian_neighbour_gen(neighbours_count, constraints, sigma, mean=0.0):

    """Creates gaussian neighbourhood generator."""

    def generate_neighbourhood(location):

        """Generates neighbourhood for given 2d location."""

        random_numbers = numpy.random.normal(mean, sigma, neighbours_count * 2)

        neighbours = []
        for i in range(neighbours_count):
            x_position = location.position_x + random_numbers[i * 2]
            x_position = adjust(x_position, constraints.min_x, constraints.max_x)
            y_position = location.position_y + random_numbers[i * 2 + 1]
            y_position = adjust(y_position, constraints.min_y, constraints.max_y)
            neighbours.append(Location2D(x_position,y_position))
        return neighbours
    return generate_neighbourhood


def adjust(x, min, max):
    while x < min or x > max:
        if x < min:
            x = 2 * min - x
        else:
            x = 2 * max - x
    return x