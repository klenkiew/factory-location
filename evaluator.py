"""Module with method to create different evaluators."""

class Evaluator(object):
    """Class evaluating goal function and counting evaluations."""
    def __init__(self, required_resources):
        self.resources = required_resources
        self.evaluations = 0

    def evaluate(self, factory_location):
        """Evaluates goal function for specified factory location."""
        score = sum([resource.required_units * resource.resource.unit_transport_cost_function(factory_location.distance(resource.resource.location))
                     for resource in self.resources])
        self.evaluations += 1
        return score
