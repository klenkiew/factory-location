"""Module with evolutionary selection functions."""
import numpy as np

class Selector(object):
    """Evolutionary algorithm selection method."""

    def select(self, population, count):
        "Selects count subjects from population."
        pass

class ProportionalSelector(Selector):
    """Proportional selector implementation"""

    def select(self, population, count):
        population_size = len(population)
        selected = []
        for i in range(count):
            selected.append(population[int(np.random.uniform(0, population_size))])
        return selected

class TournamentSelector(Selector):
    """Tournament selector implementation."""

    def __init__(self, evaluator, tournament_slots=2):
        self.evaluate = evaluator
        self.tournament_slots = tournament_slots

    def select(self, population, count):
        population_size = len(population)
        selected = []
        for i in range(count):
            best = population[int(np.random.uniform(0, population_size))]
            best_score = self.evaluate(best)
            for j in range(1, self.tournament_slots):
                enemy = population[int(np.random.uniform(0, population_size))]
                enemy_score = self.evaluate(enemy)
                if enemy_score < best_score:
                    best_score = enemy_score
                    best = enemy
            selected.append(best)
        return selected

class ThresholdSelector(Selector):
    """Threshold selector implementation."""

    def __init__(self, evaluator, threshold):
        self.evaluate = evaluator
        self.threshold = threshold

    def select(self, population, count):
        if self.threshold > len(population):
            raise Exception("Threshold higher than population size!")
        selected = []
        for i in range(count):
            selected.append(population[int(np.random.uniform(0, self.threshold))])
        return selected
