"""Module with useful utility functions."""

def is_number(value):
    """Returns true if value is a real number or false otherwise."""
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True

def is_int(value):
    """Returns true if value is integer or false otherwise."""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True

def input_with_check(message, predicate):
    """Loads value from input and performs validity check."""
    good = False
    while not good:
        value = input(message)
        if not predicate(value):
            print("Wrong data typed! Try again.")
        else:
            good = True
    return value

def interactive_mode(params, ask_for_input_file):
    """Asks user for input."""
    # algorithm predicate
    alp = lambda val: is_int(val) and (int(val) == 0 or int(val) == 1)
    # selection method predicate
    smp = lambda val: is_int(val) and (int(val) == 0 or int(val) == 1 or int(val) == 2)
    # probalbility predicate
    prp = lambda val: is_number(val) and float(val) >= 0.0 and float(val) <= 1.0
    # positive int predicate
    pip = lambda val: is_int(val) and int(val) >= 0

    if ask_for_input_file:
        params["Input_file"] = input("Select input file: ")
    print("Available algorithms:")
    print("0 - Hill climbing algorithm")
    print("1 - Evolutionary algorithm")
    params["Algorithm"] = int(input_with_check("Select algorithm to use: ", alp))
    if params["Algorithm"] == 0:
        params["Neighbourhood_size"] = int(input_with_check("Select neighbourhood size: ", pip))
    params["Neighbourhood_sigma"] = float(input_with_check("Select neighbourhood sigma: ", is_number))
    params["Neighbourhood_mean"] = float(input_with_check("Select neighbourhood mean: ", is_number))
    if params["Algorithm"] == 1:
        print("---Evolutionary algorithm parameters---")
        print("Available selection methods:")
        print("0 - proportional selection")
        print("1 - tournament selection")
        print("2 - threshold selection")
        params["Selection_method"] = int(input_with_check("Select selection method: ", smp))
        if params["Selection_method"] == 1:
            params["Tournament_size"] = int(input_with_check("Select tournament size: ", pip))
        if params["Selection_method"] == 2:
            params["Selection_threshold"] = int(input_with_check("Select selection threshold: ", pip))
        params["Population_size"] = int(input_with_check("Select population size: ", pip))
        params["Reproduction_size"] = int(input_with_check("Select reproduction size: ", pip))
        params["Crossover_probability"] = float(input_with_check("Select crossover probability: ", prp))
        params["Iterations_count"] = int(input_with_check("Select iterations count: ", pip))
    params["Start_point"][0] = float(input_with_check("Select starting point X: ", is_number))
    params["Start_point"][1] = float(input_with_check("Select starting point Y: ", is_number))
