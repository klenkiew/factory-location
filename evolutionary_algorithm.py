"""Module with evolutionary algorithm class."""
import random

import numpy as np
from algorithm import Algorithm, NullLogger, Location2D

class EvolutionaryAlgorithmOptions(object):
    """Evolutionary algorithm parameters."""

    def __init__(self, selector, population_size, reproduction_size, crossover_prob, stop_cond):
        self.population_size = population_size
        self.reproduction_size = reproduction_size
        self.selector = selector
        self.crossover_probability = crossover_prob
        self.should_stop = stop_cond

class EvolutionaryAlgorithm(Algorithm):
    """Evolutionary algorithm implementation."""

    def __init__(self, evaluator, options, neighbourhood_gen, logger=NullLogger()):
        Algorithm.__init__(self, evaluator, neighbourhood_gen, logger)
        self.options = options

    def mutation(self, subject):
        """Creates subjects mutant."""
        return self.neighbourhood_generator(subject)[0]

    def crossover(self, first, second):
        """Creates subjects crossover."""
        alfa_x = random.random()
        alfa_y = random.random()
        new_x = alfa_x * first[0].position_x + (1 - alfa_x) * second[0].position_x
        new_y = alfa_y * first[0].position_y + (1 - alfa_y) * second[0].position_y
        return Location2D(new_x, new_y)

    def run(self, start_point=Location2D()):
        # initialize population with neighbours of start_point
        population = []
        for i in range(self.options.population_size):
            new_subject = self.mutation(start_point)
            new_score = self.evaluator(new_subject)
            population.append([new_subject, new_score])
            if i == 0:
                best = new_subject
                best_score = new_score
            else:
                if new_score < best_score:
                    best_score = new_score
                    best = new_subject
        iteration = 1
        # sort population according to goal function
        population.sort(key=lambda x: x[1])
        while not self.options.should_stop(iteration, population):
            self.logger.next_iteration(iteration, best, best_score)
            reproduced = []
            for i in range(self.options.reproduction_size):
                if np.random.uniform() < self.options.crossover_probability:
                    to_cross = self.options.selector.select(population, 2)
                    new_subject = self.mutation(self.crossover(to_cross[0], to_cross[1]))
                    new_score = self.evaluator(new_subject)
                    reproduced.append([new_subject, new_score])
                else:
                    new_subject = self.mutation(self.options.selector.select(population, 1)[0][0])
                    new_score = self.evaluator(new_subject)
                    reproduced.append([new_subject, new_score])
            # elitary replacement population[-1] = best in old population
            population[0] = population[-1]
            for j in range(1, self.options.population_size - 1):
                population[j] = reproduced[j]
                if population[j][1] < best_score:
                    best_score = population[j][1]
                    best = population[j][0]
            population.sort(key=lambda x: x[1])
            iteration += 1
        return best, best_score

