"""Module with evolutionary algorithm class."""
import random

import numpy as np
from algorithm import Algorithm, NullLogger, Location2D

class EvolutionaryAlgorithmOptions(object):
    """Evolutionary algorithm parameters."""

    def __init__(self, selector, population_size, reproduction_size, crossover_prob, iterations):
        self.population_size = population_size
        self.reproduction_size = reproduction_size
        self.selector = selector
        self.crossover_probability = crossover_prob
        self.iterations = iterations

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
        new_x = alfa_x * first.position_x + (1 - alfa_x) * second.position_x
        new_y = alfa_y * first.position_y + (1 - alfa_y) * second.position_y
        return Location2D(new_x, new_y)

    def run(self, start_point=Location2D()):
        # initialize population with neighbours of start_point
        population = []
        for i in range(self.options.population_size):
            population.append(self.mutation(start_point))
            if i == 0:
                best = population[i]
                best_score = self.evaluator(best)
            else:
                subject_score = self.evaluator(population[i])
                if subject_score < best_score:
                    best_score = subject_score
                    best = population[i]
        iteration = 1
        # sort population according to goal function
        population = sorted(population, key=lambda ind: self.evaluator(ind))
        while iteration <= self.options.iterations:
            self.logger.next_iteration(iteration, best, best_score)
            reproduced = []
            for i in range(self.options.reproduction_size):
                if np.random.uniform() < self.options.crossover_probability:
                    to_cross = self.options.selector.select(population, 2)
                    reproduced.append(self.mutation(self.crossover(to_cross[0], to_cross[1])))
                else:
                    reproduced.append(self.mutation(self.options.selector.select(population, 1)[0]))
            # TODO: Maybe elite replacement too (it's only generational now)
            for j in range(self.options.population_size):
                population[j] = reproduced[j]
                subject_score = self.evaluator(population[j])
                if subject_score < best_score:
                    best_score = subject_score
                    best = population[j]
            population = sorted(population, key=lambda ind: self.evaluator(ind))
            iteration += 1
        return best, best_score

