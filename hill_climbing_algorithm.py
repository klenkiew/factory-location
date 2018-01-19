"""Module with hill climbing algorithm class."""
from algorithm import Algorithm, NullLogger, Location2D

class HillClimbingAlgorithm(Algorithm):
    """Hill climbing algorithm implementation."""

    def __init__(self, evaluator, neighbourhood_gen, stop_cond, logger=NullLogger()):
        Algorithm.__init__(self, evaluator, neighbourhood_gen, stop_cond, logger)

    def run(self, start_point=Location2D()):
        neighbourhood = []
        best = start_point
        best_score = self.evaluate(start_point)
        iteration_count = 1
        while not self.should_stop(iteration_count, [best, best_score], neighbourhood, self.evaluator.evaluations):
            neighbourhood = []
            self.logger.next_iteration(iteration_count, best, best_score)
            point_neighbourhood = self.neighbourhood_generator(best)
            for neighbour in point_neighbourhood:
                current_node_score = self.evaluate(neighbour)
                neighbourhood.append([neighbour, current_node_score])
                self.logger.next_neighbour(iteration_count, neighbour, current_node_score, best,
                                           best_score)
                if current_node_score < best_score:
                    best = neighbour
                    best_score = current_node_score
            iteration_count += 1
        return best, best_score
