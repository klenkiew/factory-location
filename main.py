"""Module with entry point for factory localization optimizer."""
import sys
import json

from hill_climbing_algorithm import HillClimbingAlgorithm
from logger import AggregateLogger, StdOutputLogger, NullLogger, PlotLogger, plt
from location import Location2D
from resource import Resource, ResourceRequirement
from neighbourhood import create_gaussian_neighbour_gen
from evaluator import Evaluator
from evolutionary_algorithm import EvolutionaryAlgorithmOptions, EvolutionaryAlgorithm
from evolutionary_selection import ProportionalSelector, TournamentSelector, ThresholdSelector
from utils import interactive_mode

def main():
    """Factory location optimizer entry point."""

    # default run parameters
    params = dict()
    params["Input_file"] = "Input.json"
    params["Tests_count"] = 20
    params["Enable_log"] = False
    params["Algorithm_config_file"] = False
    params["Algorithm"] = 0
    params["Start_point"] = [0, 0]
    params["Neighbourhood_size"] = 100
    params["Neighbourhood_sigma"] = 1.0
    params["Neighbourhood_mean"] = 0.0
    params["Resources"] = []

    # check given options
    skip = False
    for i in range(1, len(sys.argv)):
        if skip:
            skip = False
            continue
        if sys.argv[i] == "-i" or sys.argv[i] == "--input":
            if len(sys.argv) <= i + 1:
                print("Not enough arguments!")
                return
            params["Input_file"] = sys.argv[i + 1]
            skip = True
            continue
        if sys.argv[i] == "-ac" or sys.argv[i] == "--algorithm_config":
            if len(sys.argv) <= i + 1:
                print("Not enough arguments!")
                return
            params["Algorithm_config_file"] = sys.argv[i + 1]
            skip = True
            continue
        if sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print("Factory location optimizer.")
            print("Available options:")
            print("-i  --input\t\t[FileName]\tSets file with factory resources.")
            print("-ac --algorithm_config\t[FileName]\tSets file with algorithm options.")
            print("-h  --help\t\t\t\tShows help and close program.")
            print("Available algorithms:")
            print("0 - Hill climbing algorithm")
            print("1 - Evolutionary algorithm")
            print("Available selection methods (for evolutionary algorithm only):")
            print("0 - proportional selection")
            print("1 - tournament selection")
            print("2 - threshold selection")
            return
        print("Not recognized argument! Skipping...")

    # run interactive mode
    if params["Algorithm_config_file"] is False:
        interactive_mode(params, params["Input_file"] == "Input.json")
    else:
        print("Loading algorithm configuration from file: " + params["Algorithm_config_file"])
        try:
            algorithm_config = json.load(open(params["Algorithm_config_file"], 'r'))
            for key in algorithm_config.keys():
                if key == "Stop_condition":
                    func_dict = dict()
                    exec(algorithm_config[key], func_dict)
                    params[key] = func_dict["cond"]
                else:
                    params[key] = algorithm_config[key]
        except FileNotFoundError:
            print("Cannot open " + params["Algorithm_config_file"] + " file!")
            return

    print("Loading resources from: " + params["Input_file"])
    try:
        resources_json = json.load(open(params["Input_file"], 'r'))
        for res in resources_json["Resources"]:
            func_dict = dict()
            exec(res["Transport_cost_func"], func_dict)
            params["Resources"].append(ResourceRequirement(Resource(Location2D(res["Position"][0], res["Position"][1]), func_dict["f"]), res["Required_units"]))
    except FileNotFoundError:
        print("Cannot open " + params["Input_file"] + " file!")
        return
    print("Loaded " + str(len(params["Resources"])) + " resources!")

    evaluator = Evaluator(params["Resources"])
    plot_logger = PlotLogger()

    if params["Algorithm"] == 1:
        if params["Selection_method"] == 0:
            selector_obj = ProportionalSelector()
        if params["Selection_method"] == 1:
            selector_obj = TournamentSelector(params["Tournament_size"])
        if params["Selection_method"] == 2:
            selector_obj = ThresholdSelector(params["Selection_threshold"])

    if params["Algorithm"] == 0:
        algorith_name = "Hill climbing algorithm"
    else:
        algorith_name = "Evolutionary algorithm"

    if params["Enable_log"]:
        logger = AggregateLogger([StdOutputLogger(algorith_name), plot_logger])
    else:
        logger = NullLogger()

    if params["Algorithm"] == 0:
        algorithm = HillClimbingAlgorithm(evaluator,
                                          create_gaussian_neighbour_gen(params["Neighbourhood_size"], params["Neighbourhood_sigma"], params["Neighbourhood_mean"]),
                                          params["Stop_condition"], logger)
    else:
        options = EvolutionaryAlgorithmOptions(selector_obj, params["Population_size"], params["Reproduction_size"],
                                               params["Crossover_probability"])
        algorithm = EvolutionaryAlgorithm(evaluator, options,
                                        create_gaussian_neighbour_gen(1, params["Neighbourhood_sigma"], params["Neighbourhood_mean"]),
                                        params["Stop_condition"], logger)

    results = []
    average_goal_func = 0.0
    for i in range(params["Tests_count"]):
        logger.clear()
        results.append(algorithm.run(Location2D(params["Start_point"][0], params["Start_point"][1])))
        average_goal_func += results[i][1]
        if params["Enable_log"]:
            print("Best location: ({}, {}) [{}]".format(results[i][0].position_x,
                                                        results[i][0].position_y,
                                                        results[i][1]))
            print("Evaluations count: {}".format(evaluator.evaluations))
            # draw goal function plot
            plot_logger.draw("Goal function")
            # draw resources and factory location
            # resources as green dots and factory as red dot
            for res in params["Resources"]:
                plt.plot(res.resource.location.position_x, res.resource.location.position_y, "go")
            plt.plot(results[i][0].position_x, results[i][0].position_y, "ro")
            plt.xlabel("Position X")
            plt.ylabel("Position Y")
            plt.title("Resources and factory location")
            plt.show()


    average_goal_func /= params["Tests_count"]
    print("Average goal function: {0:.4f}".format(average_goal_func))


if __name__ == '__main__':
    main()
