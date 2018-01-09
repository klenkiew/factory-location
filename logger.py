import matplotlib.pyplot as plt


class StandardOutputLogger:
    def next_iteration(self, iteration_count, best, best_score):
        print("[Hill climbing algorithm] Iteration: {0} Best: ({1:.2f}, {2:.2f}) [{3:.2f}]"
              .format(iteration_count, best.x, best.y, best_score))

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        print("[Hill climbing algorithm] Iteration: {0} Best: ({1:.2f}, {2:.2f}) [{3:.2f}] "
              "Neighbour: ({4:.2f}, {5:.2f}) [{6:.2f}]"
              .format(iteration_count, best.x, best.y, best_score, neighbour.x, neighbour.y, current_node_score))


class PlotLogger:
    def __init__(self):
        self.results = []

    def next_iteration(self, iteration_count, best, best_score):
        self.results.append((iteration_count, best_score))

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        pass

    def draw(self):
        plt.plot([result[0] for result in self.results], [result[1] for result in self.results],
                 color='lightblue', linewidth=3)
        plt.xlabel("Iteration")
        plt.ylabel("Best result")
        plt.show()


class AggregateLogger:
    def __init__(self, loggers):
        self.loggers = loggers

    def next_iteration(self, iteration_count, best, best_score):
        for logger in self.loggers:
            logger.next_iteration(iteration_count, best, best_score)

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        for logger in self.loggers:
            logger.next_neighbour(iteration_count, neighbour, current_node_score, best, best_score)
