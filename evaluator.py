"""Module with method to create different evaluators."""

def create_evaluator(required_resources):
    """Creates evaluator for goal function."""

    def evaluate(factory_location):
        """Evaluates goal function for specified factory location."""
        return sum([required_units * resource.unit_transport_cost_function(factory_location.distance(resource.location))
                    for resource, required_units in required_resources])
    return evaluate
