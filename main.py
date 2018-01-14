import sys

from evolutionary_algorithm import *
from hill_climbing_algorithm import *
from logger import *
from location import Location
from resource import Resource


NEIGHBOURS_COUNT = 100


def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def main():
    if len(sys.argv) != 2:
        print("Please enter an input file name")
        return

    resources = []
    with open(sys.argv[1], 'r') as input_file:
        lines = input_file.readlines()
        non_comment_lines = filter(lambda l: l[0] != '#', lines)
        for line in non_comment_lines:
            # file format: resource x coord, resource y coord, required units, transport cost function
            # separated with spaces
            split = line.split(" ", 3)
            location = Location(float(split[0]), float(split[1]))
            required_units = float(split[2])
            func_dict = {}
            # create a function from string
            # TODO: it can't handle multi-line functions
            exec(split[3], func_dict)
            # extract the function
            transport_cost_func = func_dict.popitem()[1]
            # check that the result type is correct (should be a number)
            result = transport_cost_func(0)
            if not is_number(result):
                print("Wrong type of function result")
                return
            resources.append((Resource(location, transport_cost_func), required_units))

    run_hill_climbing_algorithm(resources)
    run_evolutionary_algorithm(resources)


def run_evolutionary_algorithm(resources):
    algorothm = EvolutionaryAlgorithm(create_tournament_selection(2), crossover, create_mutator(1),
                                      create_replace_function(create_evaluator(resources)),
                                      lambda iter, pop: iter == 100, 0.2)
    result = algorothm.run([Location(0, 0) for _ in range(20)]).best_individual
    print("[HillClimbing] Best location: ({}, {}) [{}]".format(result.value.x, result.value.y, result.fitness))


def run_hill_climbing_algorithm(resources):
    plot_logger = PlotLogger()
    algorithm = HillClimbingAlgorithm(create_evaluator(resources),
                                      create_gaussian_neighbourhood_generator(NEIGHBOURS_COUNT, 1),
                                      AggregateLogger([StandardOutputLogger(), plot_logger]))
    result = algorithm.run(Location(0, 0))
    print("[EvolutionaryAlgorithm] Best location: ({}, {}) [{}]".format(result[0].x, result[0].y, result[1]))
    plot_logger.draw()


if __name__ == '__main__':
    main()
