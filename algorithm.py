"""Module with optimization algorithm base class."""
from logger import NullLogger
from location import Location2D

class Algorithm(object):
    """Base class representing oprimization algorithm."""

    def __init__(self, evaluator, neighbourhood_gen, logger=NullLogger()):
        self.evaluator = evaluator
        self.neighbourhood_generator = neighbourhood_gen
        self.logger = logger

    def run(self, start_point=Location2D()):
        """Runs optimization algorithm starting from given point."""
        pass
