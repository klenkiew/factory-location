"""Module with evolutionary selection functions."""
import random

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
            selected.append(population[random.randint(0, population_size)])
        return selected

class TournamentSelector(Selector):
    """Tournament selector implementation."""

    def __init__(self, tournament_slots=2):
        self.tournament_slots = tournament_slots

    def select(self, population, count):
        population_size = len(population)
        selected = []
        for i in range(count):
            best = population[random.randint(0, population_size)]
            best_score = best[1]
            for j in range(1, self.tournament_slots):
                enemy = population[random.randint(0, population_size)]
                enemy_score = enemy[1]
                if enemy_score < best_score:
                    best_score = enemy_score
                    best = enemy
            selected.append(best)
        return selected

class ThresholdSelector(Selector):
    """Threshold selector implementation."""

    def __init__(self, threshold):
        self.threshold = threshold

    def select(self, population, count):
        if self.threshold > len(population):
            raise Exception("Threshold higher than population size!")
        selected = []
        for i in range(count):
            selected.append(population[random.randint(0, self.threshold)])
        return selected
