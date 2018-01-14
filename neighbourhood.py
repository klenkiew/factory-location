"""Module with neighbourhood creation functions."""
import numpy
from location import Location2D


def create_gaussian_neighbour_gen(neighbours_count, sigma, mean=0.0):
    """Creates gaussian neighbourhood generator."""

    def generate_neighbourhood(location):
        """Generates neighbourhood for given 2d location."""

        random_numbers = numpy.random.normal(mean, sigma, neighbours_count * 2)
        neighbours = []
        for i in range(neighbours_count):
            neighbours.append(Location2D(location.position_x + random_numbers[i*2],
                                         location.position_y + random_numbers[i*2 + 1]))
        return neighbours
    return generate_neighbourhood
