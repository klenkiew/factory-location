"""Module with evolutionary algorithm class."""
from algorithm import Algorithm, NullLogger

# TODO: Write evolutionary algorithm implementation
class EvolutionaryAlgorithm(Algorithm):
    """Evolutionary algorithm implementation."""
    def __init__(self, evaluator, neighbourhood_gen, logger=NullLogger()):
        Algorithm.__init__(self, evaluator, neighbourhood_gen, logger)

