from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Tuple
import random

T = TypeVar('T')

class IGeneticProblem(ABC):
    @abstractmethod
    def generate_initial_population(population_size : int) -> List[T]:
        pass

    @abstractmethod
    def fitness(self, obj : T) -> float:
        pass

    @abstractmethod
    def crossover(self, objA : T, objB : T) -> T:
        pass

    @abstractmethod
    def mutate(self, obj : T) -> T:
        pass

    @abstractmethod
    def stop_criterium(self, generation : List[T]) -> bool:
        pass

    def offspring(self, actual : List[T], population_size : int, crossover_rate : float) -> List[T]:
        new_generation = [self.duplicate(agent) for agent in actual[ : int(len(actual)*(1-crossover_rate))]]
        mix_blood = []
        for i in range(population_size - len(new_generation)):
            parentA, parentB = random.choices(new_generation, k=2)
            mix_blood.append(self.crossover(parentA, parentB))
        for i in range(len(mix_blood)):
            mix_blood[i] = self.mutate(mix_blood[i])
        new_generation.extend(mix_blood)
        new_generation.sort(key= self.fitness, reverse= True)
        return new_generation
    
    @abstractmethod
    def duplicate(self, obj : T) -> T:
        pass
    
    def simple_run(self, crossover_rate : float, population_size : int) -> Tuple[int, List[T]]:
        """Retorna el numero de simulaciones para el que se llego a la respuesta y ademas la
        poblacion final"""
        population = self.generate_initial_population(population_size)
        population.sort(key= self.fitness, reverse= True)
        iteration = 0
        while not self.stop_criterium(population):
            population = self.offspring(population, population_size, crossover_rate)
            iteration = iteration + 1
        return iteration, population