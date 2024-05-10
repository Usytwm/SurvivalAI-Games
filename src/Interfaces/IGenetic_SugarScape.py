import sqlite3
import numpy
import random
import matplotlib.pyplot as plt
from abc import abstractmethod, ABC
from ai.search.genetic.IGeneticProblem import IGeneticProblem
from agents.ProAgent.pro_agent import ProAgent
from Interfaces.IAgent import IAgent
from environment.map import Map
from environment.simple_simulation import SimpleSimulation
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision, SquareAttackRange
from typing import Dict, List, Tuple

from agents.CombatantAgent.CombatantAgent import CombatantAgent
from agents.ExpertAgent.expert_agent import ExpertAgent
from agents.RandomAgent.random_agent import RandomAgent
from agents.FoodSeekerAgent.FoodSeekerAgent import FoodSeekerAgent
from agents.FoodSeekerAgentwithAstar.FoodSeekerAgentwithAstar import FoodSeekerAgentwithAstar
from agents.PacifistAgent.PacifistAgent import PacifistAgent


class IGenetic_SugarScape(IGeneticProblem):
    """Usamos esta clase para modelar cualquier problema genetico cuya funcion de fitness sea 
    la cantidad de rondas que un agente sobrevivio"""
    def __init__(self):
        #population contiene la poblacion actual
        #rankings es un diccionario donde a cada id de agente le hacemos corresponder la ronda
        #en que fue eliminado en la ultima simulacion
        self.initial_population : List[IAgent] = None
        self.generate_initial_population(20)
        self.population = self.initial_population.copy()
        self.rankings : Dict[int, int] = {}
        self.rankings_calculated = False
        self.ids_to_replace : List[int] = []
    
    def fitness(self, agent : ProAgent) -> int:
        """Devuelve cuantas rondas sobrevivio el agente"""
        if not self.rankings_calculated:
            self.simulate()
            self.rankings_calculated = True
        try:
            return self.rankings[agent.id]
        except:
            return 0
    
    def generate_initial_population(self, population_size: int) -> List[IAgent]:
        if not self.initial_population:
            self.initial_population = self.__generate_initial_population__(population_size)
        return self.initial_population
    
    @abstractmethod
    def __generate_initial_population__(population_size : int):
        pass
    
    def simulate(self):
        resources = {}
        for i in range(20):
            for j in range(20):
                if random.choices([True, False]):
                    resources[(i, j)] = random.randint(1, 100)
        map = Map(20, 20, resources)
        positions = set()
        while len(positions) < 100:
            new_position = (random.randint(0, 19), random.randint(0, 19))
            if not new_position in positions:
                positions.add(new_position)
        positions = list(positions)
        agents = self.create_agents_for_simulation(positions, map)
        simulation = SimpleSimulation(map, agents)
        iteration = 1
        while not simulation.__has_ended__():
            for agent_id in simulation.step():
                self.rankings[agent_id] = iteration
            iteration += 1
            if iteration == 1000:
                break
        tuples_agent_death = list(self.rankings.items())
        tuples_agent_death.sort(key= lambda tpl : tpl[1], reverse= True)
        tuples_agent_death = [x for x in tuples_agent_death if x[0] <= 20]
        self.ids_to_replace = [x[0] for x in tuples_agent_death[5 : ]]

    def create_agents_for_simulation(self, positions : List[Tuple[int, int]], map : Map) -> List[Tuple[Tuple[int] | Tuple[int | Agent_Handler]]]:
        answer = []
        idx = 0
        for agent in self.population:
            agent = self.duplicate(agent)
            agent.reserves = random.randint(0, 100)
            handler = Agent_Handler(idx + 1, agent.reserves, 1, map, agent, SimpleWalking(), SquareVision(3), SquareAttackRange(3))
            answer.append((positions[idx], (idx + 1, handler)))
            idx += 1
        for agent_id in range(21, 100):
            reserves = random.randint(1, 100)
            agent = random.choice(
                [
                    FoodSeekerAgentwithAstar(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                    PacifistAgent(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                    FoodSeekerAgent(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                    RandomAgent(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                    CombatantAgent(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                    #ExpertAgent(agent_id, 1, reserves, sqlite3.connect(":memory:")),
                ]
            )
            handler = Agent_Handler(agent_id, random.randint(1, 100), 1, map, agent, SimpleWalking(), SquareVision(3), SquareAttackRange(3))
            answer.append((positions[agent_id - 1], (agent_id, handler)))
        
        return answer