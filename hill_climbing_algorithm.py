import numpy
from location import Location


class NullLogger:
    def next_iteration(self, iteration_count, best, best_score):
        pass

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        pass


class HillClimbingAlgorithm:
    def __init__(self, evaluator, neighbourhood_generator, logger=NullLogger()):
        self.evaluator = evaluator
        self.neighbourhood_generator = neighbourhood_generator
        self.logger = logger

    def run(self, start_point):
        best = start_point
        best_score = self.evaluator(start_point)
        best_changed = True
        iteration_count = 1
        while best_changed:
            self.logger.next_iteration(iteration_count, best, best_score)
            best_changed = False
            neighbourhood = self.neighbourhood_generator(best)
            for neighbour in neighbourhood:
                current_node_score = self.evaluator(neighbour)
                self.logger.next_neighbour(iteration_count, neighbour, current_node_score, best, best_score)
                if current_node_score < best_score:
                    best = neighbour
                    best_score = current_node_score
                    best_changed = True
            iteration_count += 1
        return best, best_score


def create_evaluator(required_resources):
    def evaluate(factory_location):
        return sum([required_units * resource.unit_transport_cost_function(factory_location.distance(resource.location))
                    for resource, required_units in required_resources])
    return evaluate


def create_gaussian_neighbourhood_generator(neighbours_count, sigma, mean=0.0):
    def generate_neighbourhood(location):
        random_numbers = numpy.random.normal(mean, sigma, neighbours_count * 2)
        neighbours = []
        for i in range(neighbours_count):
            neighbours.append(Location(location.x + random_numbers[i], location.y + random_numbers[i + 1]))
        return neighbours
    return generate_neighbourhood
