"""Module with random resource generator."""
import argparse
import inspect
import random
import json

from location import Location2D
from resource import Resource, ResourceRequirement


def main():
    """Random resource generator entry point."""
    parser = argparse.ArgumentParser(description='A simple program to generate data for factory location problem.')
    parser.add_argument('min_pos', type=float, help="Minimum value for resources location")
    parser.add_argument('max_pos', type=float, help="Maximum value for resources location")
    parser.add_argument('min_req_units', type=float, help="Minimum value for required units")
    parser.add_argument('max_req_units', type=float, help="Maximum value for required units")
    parser.add_argument('min_resources', type=int, help="Minimum number of resources")
    parser.add_argument('max_resources', type=int, help="Maximum number of resources")
    args = parser.parse_args()
    resources = generate_random_resources(args)

    # main json object
    json_main_obj = dict()
    json_main_obj["Resources"] = []

    print("# Generated resources: ")
    for resource_requirement in resources:
        resource = resource_requirement.resource
        resource_location = resource.location
        function_string = function_to_string(resource)
        print("{} {} {} {}".format(resource_location.position_x,
                                   resource_location.position_y,
                                   resource_requirement.required_units,
                                   function_string))
        # prepare object to save
        json_res = dict()
        json_res["Position"] = [resource_location.position_x, resource_location.position_y]
        json_res["Required_units"] = resource_requirement.required_units
        json_res["Transport_cost_func"] = function_string
        json_main_obj["Resources"].append(json_res)

    # save to file
    # TODO: not const filename
    json.dump(json_main_obj, open("Out.json", 'w'), indent=4)


def generate_random_resources(args):
    """Function which generates random resources with given constraints"""
    resource_count = random.randint(args.min_resources, args.max_resources)
    resources = []
    for i in range(resource_count):
        resource_position_x = random.uniform(args.min_pos, args.max_pos)
        resource_position_y = random.uniform(args.min_pos, args.max_pos)
        required_units = random.uniform(args.min_req_units, args.max_req_units)
        transport_cost_function = get_random_function()
        resource = Resource(Location2D(resource_position_x, resource_position_y), transport_cost_function)
        resource_requirement = ResourceRequirement(resource, required_units)
        resources.append(resource_requirement)
    return resources


def get_random_function():
    """Returns random function."""
    # TODO generate random non-linear functions
    def f(d): return d
    return f


def function_to_string(resource):
    """Changes function to string."""
    function_source_lines = inspect.getsourcelines(resource.unit_transport_cost_function)
    function_string = "".join((function_source_lines[0]))
    # remove leading and trailing whitespaces to prevent empty lines
    return function_string.strip()


if __name__ == "__main__":
    main()
