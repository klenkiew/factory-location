"""Module with hill climbing algorithm class."""
from algorithm import Algorithm, NullLogger, Location2D

class HillClimbingAlgorithm(Algorithm):
    """Hill climbing algorithm implementation."""

    def __init__(self, evaluator, neighbourhood_gen, logger=NullLogger()):
        Algorithm.__init__(self, evaluator, neighbourhood_gen, logger)

    def run(self, start_point=Location2D()):
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
                self.logger.next_neighbour(iteration_count, neighbour, current_node_score, best,
                                           best_score)
                if current_node_score < best_score:
                    best = neighbour
                    best_score = current_node_score
                    best_changed = True
            iteration_count += 1
        return best, best_score
