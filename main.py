"""Module with entry point for factory localization optimizer."""
import sys

from hill_climbing_algorithm import HillClimbingAlgorithm
from logger import AggregateLogger, StdOutputLogger, PlotLogger, plt
from location import Location2D
from resource import Resource
from neighbourhood import create_gaussian_neighbour_gen
from evaluator import create_evaluator
from evolutionary_algorithm import EvolutionaryAlgorithmOptions, EvolutionaryAlgorithm
from evolutionary_selection import ProportionalSelector, TournamentSelector, ThresholdSelector


NEIGHBOURS_COUNT = 100


def is_number(value):
    """Returns true if value is a real number or false otherwise."""
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True

def is_int(value):
    """Returns true if value is integer or false othervise."""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def main():
    """Factory location optimizer entry point."""
    if len(sys.argv) != 3:
        print "Please enter an input file name and select algorithm."
        print "Available algorithms:"
        print "0 - Hill climbing algorithm"
        print "1 - Evolutionary algorithm"
        return

    if not is_int(sys.argv[2]) or int(sys.argv[2]) > 1 or int(sys.argv[2]) < 0:
        print "Second argument is not valid algorithm number!"
        return

    selected_algorithm = int(sys.argv[2])

    start = input("Select start point (Location2D(x, y)): ")
    if selected_algorithm != 1:
        neighbours = input("Neighbourhood size: ")
    neighbours_sigma = input("Neighbourhood sigma: ")
    neighbours_mean = input("Neighbourhood mean: ")

    if selected_algorithm == 1:
        print "---Evolutionary algorithm parameters---"
        print "Available selection methods:"
        print "0 - proportional selection"
        print "1 - tournament selection"
        print "2 - threshold selection"
        selector = input("Select selection method: ")
        if selector == 1:
            tournament_size = input("Select tournament size: ")
        if selector == 2:
            threshold = input("Select threshold: ")
        pop_size = input("Select population size: ")
        rep_size = input("Select reproduction size: ")
        cross = input("Select crossover probability (0.0 - 1.0): ")
        iterations_count = input("Select iterations count: ")

    resources = []
    with open(sys.argv[1], 'r') as input_file:
        lines = input_file.readlines()
        non_comment_lines = [l for l in lines if l[0] != "#"]
        for line in non_comment_lines:
            # file format: resource x coord, resource y coord,
            # required units, transport cost function separated
            # with spaces
            split = line.split(" ", 3)
            location = Location2D(float(split[0]), float(split[1]))
            required_units = float(split[2])
            func_dict = {}
            # create a function from string
            # TODO: it can't handle multi-line functions
            exec(split[3], func_dict)
            # extract the function
            transport_cost_func = func_dict["func"]
            # check that the result type is correct (should be a number)
            result = transport_cost_func(0)
            if not is_number(result):
                print "Wrong type of function result"
                return
            resources.append((Resource(location, transport_cost_func), required_units))

    evaluator = create_evaluator(resources)
    plot_logger = PlotLogger()

    if selected_algorithm == 1:
        if selector == 0:
            selector_obj = ProportionalSelector()
        if selector == 1:
            selector_obj = TournamentSelector(evaluator, tournament_size)
        if selector == 2:
            selector_obj = ThresholdSelector(evaluator, threshold)

    if selected_algorithm == 0:
        algorithm = HillClimbingAlgorithm(evaluator,
                                          create_gaussian_neighbour_gen(neighbours, neighbours_sigma, neighbours_mean),
                                          AggregateLogger([StdOutputLogger("Hill climbing algorithm"), plot_logger]))
    else:
        options = EvolutionaryAlgorithmOptions(selector_obj, pop_size, rep_size, cross, iterations_count)
        algorithm = EvolutionaryAlgorithm(evaluator, options,
                                        create_gaussian_neighbour_gen(1, neighbours_sigma, neighbours_mean),
                                        AggregateLogger([StdOutputLogger("Evolutionary algorithm"), plot_logger]))
    result = algorithm.run(start)
    print "Best location: ({}, {}) [{}]".format(result[0].position_x,
                                                result[0].position_y,
                                                result[1])
    # draw goal function plot
    plot_logger.draw("Goal function")
    # draw resources and factory location
    # resources as green dots and factory as red dot
    for res in resources:
        plt.plot(res[0].location.position_x, res[0].location.position_y, "go")
    plt.plot(result[0].position_x, result[0].position_y, "ro")
    plt.xlabel("Position X")
    plt.ylabel("Position Y")
    plt.title("Resources and factory location")
    plt.show()


if __name__ == '__main__':
    main()
