import sqlite3
from typing import List, Tuple
from Interfaces.IAgent import IAgent
from environment.sim_object import Object_Info
from memory.memory_for_agents_sights import Memory_for_Agents_Sights
from memory.geographic_memory import Geographic_Memory
class Agent_with_Memories(IAgent):
    def __init__(self, id : int, consume : int, reserves, conn : sqlite3.Connection):
        self.id = id
        self.consume = consume
        self.reserves = reserves
        self.position = (0, 0)
        self.iteration = 0
        self.geographic_memory = Geographic_Memory(id)
        self.memory_for_agents_sights = Memory_for_Agents_Sights(id, conn)
    
    #En IAgent deberiamos cambiar el nombre del parametro position por movement
    def inform_move(self, position: Tuple[int, int]) -> None:
        self.position = (self.position + position[0], self.position + position[1])
    
    def see_objects(self, info: List[Object_Info]) -> None:
        for sight in info:
            other_id = sight.id
            row = sight.position[0] + self.position[0]
            column = sight.position[1] + self.position[1]
            resources = 0 #Tenemos que incluir la cantidad de azucar que lleva el agente en el Object_Info
            self.memory_for_agents_sights.add_appearence(other_id, row, column, resources)
            self.geographic_memory.add_position(row, column)
        self.iteration = self.iteration + 1
    
    def see_resources(self, info: List[Tuple[Tuple[int] | int]]) -> None:
        for row, column, sugar in info:
            row = row + self.position[0]
            column = column + self.position[1]
            self.geographic_memory.add_sugar_observation(row, column, self.iteration, sugar)