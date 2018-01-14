import random

import numpy

from location import Location


class EvolutionaryAlgorithm:
    def __init__(self, selection, crossover, mutation, replacement, stop_condition, crossover_rate):
        self.mutate = mutation
        self.crossover = crossover
        self.select = selection
        self.replace = replacement
        self.should_stop = stop_condition
        self.crossover_rate = crossover_rate

    def run(self, initial_population):
        current_population = self.replace(None, initial_population)
        iteration_count = 1
        while not self.should_stop(iteration_count, current_population):
            new_population = []
            for i in range(len(initial_population)):
                if random.random() < self.crossover_rate:
                    first_parent = self.select(current_population)
                    second_parent = self.select(current_population)
                    individual = self.mutate(self.crossover(first_parent, second_parent))
                else:
                    individual = self.mutate(self.select(current_population))
                new_population.append(individual)
            current_population = self.replace(current_population, new_population)
            iteration_count += 1
        return current_population


class Individual:
    def __init__(self, location, fitness):
        self.value = location
        self.fitness = fitness


class Population:
    def __init__(self, individuals, best_individual, total_fitness):
        self.individuals = individuals
        self.best_individual = best_individual
        self.total_fitness = total_fitness


def create_tournament_selection(tournament_size):
    def tournament_selection(population):
        tournament_participants = list(map(lambda _: random.choice(population.individuals), range(tournament_size)))
        # we minimize fitness
        return min(tournament_participants, key=lambda ind: ind.fitness).value
    return tournament_selection


# TODO works for maximization, we need to minimize fitness
# (which is total cost # of transporting all resources to the factory)
# proportionate selection
def select(population):
    rand = random.uniform(0.0, population.total_fitness)
    for individual in population.individuals:
        rand -= individual.fitness
        if rand < 0:
            return individual.value
    # should only happen if rounding errors occur, the last population individual is returned
    return population.individuals[-1].value


# intermediate recombination
def crossover(first_location, second_location):
    alfa_x = random.random()
    alfa_y = random.random()
    new_x = alfa_x * first_location.x + (1 - alfa_x) * second_location.x
    new_y = alfa_y * first_location.y + (1 - alfa_y) * second_location.y
    return Location(new_x, new_y)


# gaussian mutation
def create_mutator(sigma, mean=0.0):
    def mutate(location):
        random_numbers = numpy.random.normal(mean, sigma, 2)
        return Location(location.x + random_numbers[0], location.y + random_numbers[1])
    return mutate


def create_replace_function(fitness_evaluator):
    def replace_population(old_population, new_locations):
        new_population = []
        best_individual = old_population.best_individual if old_population else Individual(None, float('inf'))
        total_fitness = 0.0
        for location in new_locations:
            # new population individuals are not evaluated yet, so we do it here
            fitness = fitness_evaluator(location)
            individual = Individual(location, fitness)
            total_fitness += individual.fitness
            # fitness is a cost function in our case, so we minimize it
            if individual.fitness < best_individual.fitness:
                best_individual = individual
            new_population.append(individual)
        # population must be sorted for roulette wheel selection to work properly
        new_population.sort(key=lambda ind: ind.fitness)
        return Population(new_population, best_individual, total_fitness)
    return replace_population
