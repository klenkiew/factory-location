"""Module with different logger types."""
import matplotlib.pyplot as plt

class NullLogger(object):
    """Base logger class. Do not output any data."""

    def next_iteration(self, iteration_count, best, best_score):
        """Method called to output next iteration data."""
        pass

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        "Method called to output itaration data with generated neighbour data."
        pass

    def clear(self):
        """Clears logger log if any."""
        pass

class StdOutputLogger(NullLogger):
    """Logger outputting information to standard output."""

    def __init__(self, name=""):
        self.logger_name = name

    def next_iteration(self, iteration_count, best, best_score):
        print("[{0}] Iteration: {1} Best: ({2:.2f}, {3:.2f}) [{4:.2f}]"
              .format(self.logger_name, iteration_count, best.position_x, best.position_y, best_score))

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        print("[{0}] Iteration: {1} Best: ({2:.2f}, {3:.2f}) [{4:.2f}] "
              "Neighbour: ({5:.2f}, {6:.2f}) [{7:.2f}]"
              .format(self.logger_name, iteration_count, best.position_x, best.position_y,
                      best_score, neighbour.position_x, neighbour.position_y, current_node_score))


class PlotLogger(NullLogger):
    """Logger outputting information to plot."""

    def __init__(self):
        self.results = []

    def next_iteration(self, iteration_count, best, best_score):
        self.results.append((iteration_count, best_score))

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        pass

    def clear(self):
        self.results = []

    def draw(self, plot_name="Created plot"):
        """Draws plot created from logged data."""
        plt.plot([result[0] for result in self.results], [result[1] for result in self.results],
                 color='lightblue', linewidth=3)
        plt.xlabel("Iteration")
        plt.ylabel("Best result")
        plt.title(plot_name)
        plt.show()


class AggregateLogger(NullLogger):
    """Logger logging data into all specified loggers at once."""

    def __init__(self, loggers):
        self.loggers = loggers

    def next_iteration(self, iteration_count, best, best_score):
        for logger in self.loggers:
            logger.next_iteration(iteration_count, best, best_score)

    def next_neighbour(self, iteration_count, neighbour, current_node_score, best, best_score):
        for logger in self.loggers:
            logger.next_neighbour(iteration_count, neighbour, current_node_score, best, best_score)

    def clear(self):
        for log in self.loggers:
            log.clear()
