"""Module with entry point for factory localization optimizer."""
import sys

from hill_climbing_algorithm import HillClimbingAlgorithm
from logger import AggregateLogger, StdOutputLogger, PlotLogger, plt
from location import Location2D
from resource import Resource
from neighbourhood import create_gaussian_neighbour_gen
from evaluator import create_evaluator


NEIGHBOURS_COUNT = 100


def is_number(value):
    """Returns true if value is a real number or false otherwise."""
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def main():
    """Factory location optimizer entry point."""
    if len(sys.argv) != 2:
        print "Please enter an input file name"
        return

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

    plot_logger = PlotLogger()
    algorithm = HillClimbingAlgorithm(create_evaluator(resources),
                                      create_gaussian_neighbour_gen(NEIGHBOURS_COUNT, 1),
                                      AggregateLogger([StdOutputLogger("Hill climbing algorithm"),
                                                       plot_logger]))
    result = algorithm.run()
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
