import argparse
import inspect
import random

from location import Location2D
from resource import Resource, ResourceRequirement


def main():
    parser = argparse.ArgumentParser(description='A simple program to generate data for factory location problem.')
    parser.add_argument('min_pos', type=float, help="Minimum value for resources location")
    parser.add_argument('max_pos', type=float, help="Maximum value for resources location")
    parser.add_argument('min_req_units', type=float, help="Minimum value for required units")
    parser.add_argument('max_req_units', type=float, help="Maximum value for required units")
    parser.add_argument('min_resources', type=int, help="Minimum number of resources")
    parser.add_argument('max_resources', type=int, help="Maximum number of resources")
    args = parser.parse_args()
    resources = generate_random_resources(args)

    print("# Generated resources: ")
    for resource_requirement in resources:
        resource = resource_requirement.resource
        resource_location = resource.location
        function_string = function_to_string(resource)
        print("{} {} {} {}".format(resource_location.position_x,
                                   resource_location.position_y,
                                   resource_requirement.required_units,
                                   function_string))


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
    # TODO generate random non-linear functions
    def func(d): return d
    return func


def function_to_string(resource):
    function_source_lines = inspect.getsourcelines(resource.unit_transport_cost_function)
    function_string = "".join((function_source_lines[0]))
    # remove leading and trailing whitespaces to prevent empty lines
    return function_string.strip()


if __name__ == "__main__":
    main()
