import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/Interfaces')
from environment.map import Map
from environment.agent_handler import Agent_Handler
from typing import List, Dict, Set, Tuple
from random import randint
from abc import ABC, abstractmethod

class ISimulation(ABC):
    def __init__(self, map : Map, agents : List[Tuple[Tuple[int, int], Tuple[int, Agent_Handler]]]):
        """Recibe los siguientes argumentos:
        - Un mapa ya creado
        - Una diccionario que a cada llave hace corresponder el handler del agente con ese id.
        El handler de cada agente debe tener asociado el mapa global.
        - Una funcion priority que compara dos agentes, para determinar cual va primero
        """
        self.map = map
        self.agents = {}
        self.objects = self.agents.copy() #Por ahora los unicos objetos que consideramos en la sim son agentes
        for position, (id, agent) in agents:
            self.map.insert(position, id)
            self.agents[id] = agent
            self.objects[id] = agent
    
    def step(self):
        "Move the simulation one step"
        self.display()
        input()
        self.__actualize_agents_vision__()
        #Pick actions from agents
        #Process actions from agents
        #Actualize each agent state
        moves = self.__get_moves__()
        self.__execute_moves__(moves)

    def __actualize_agents_vision__(self):
        "Passes to all the agents the info about what they can see"
        for agent in self.agents.values():
            print("Agent " + str(agent.id) + " in position " + str(self.map.peek_id(agent.id)) + "sees:")
            agent.see(self.objects)

    @abstractmethod
    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        """Get the moves from all players. Returns a dictionary corresponding a destiny for each
        moving agent"""
        pass

    def __execute_moves__(self, moves : Dict[int, Tuple[int, int]]):
        "Move each agent to its destination"
        for id, destiny in moves.items():
            self.map.move(id, destiny)
            self.agents[id].inform_move(destiny)
    
    @abstractmethod
    def display(self):
        "Shows whats happening"
        pass