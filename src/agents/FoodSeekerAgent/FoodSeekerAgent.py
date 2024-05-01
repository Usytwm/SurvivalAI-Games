from random import random
import sqlite3
from typing import Dict, List, Tuple
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info, Association_Proposal, Attack
from environment.sim_object import Object_Info
from ai.search.pathFinder_with_Astar import PathFinder


class FoodSeekerAgent(Agent_with_Memories):
    """Este agente selecciona la casilla que mas azucar tiene de las que conoce, y fija
    trayectoria hacia ella. Sigue la trayectoria fijada mientras ningun otro agente coma el
    azucar que hay en la casilla de destino. Una vez que llega al destino, u otro agente llega
    primero, fija otro objetivo y se mueve hacia el."""
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        super().__init__(id, consume, reserves, conn, movement, attack_range)
        self.color = (0, 255, 0)  # Green
        self.curse_fixed : List[Tuple[int, int]] = None #Lista de posiciones a visitar
        self.destination : Tuple[int, int] = None
        self.initial_sugar_in_destination : int = None
        self.path_finder = PathFinder(self.geographic_memory.validate_position)

    def move(self):
        if (not self.destination):
            self.__find_destination__()
        else:
            actual_sugar_in_destination = self.geographic_memory.get_last_info_of_sugar_in_position(self.destination[0], self.destination[1])[1]
            if actual_sugar_in_destination < self.initial_sugar_in_destination:
                self.__find_destination__()
        move = (self.curse_fixed[0][0] - self.position[0], self.curse_fixed[0][1] - self.position[1])
        return move

    def __find_destination__(self):
        self.destination, self.initial_sugar_in_destination = self.geographic_memory.get_position_with_most_sugar(self.position[0], self.position[1])
        self.curse_fixed = self.path_finder.a_star(self.position, self.destination, self.movement.pure_moves())
        self.curse_fixed.pop(0)

    def inform_move(self, movement: Tuple[int, int]):
        super().inform_move(movement)
        if self.position == self.curse_fixed[0]:
            self.curse_fixed.pop(0)

    def inform_position(self, position: Tuple[int, int] = None):
        pass

    def get_attacks(self) -> List[Action]:
        return []

    def get_association_proposals(self) -> List:
        return []
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        return False