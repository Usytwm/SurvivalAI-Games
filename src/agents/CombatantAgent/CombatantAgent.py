from random import random
import sqlite3
from typing import Dict, List, Tuple
from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info, Association_Proposal, Attack
from environment.sim_object import Object_Info
from Interfaces.IAttack_Range import IAttackRange
from Interfaces.IMovement import IMovement


class CombatantAgent(Agent_with_Memories):
    """Este agente selecciona una victima y la persigue y ataca exclusivamente a ella hasta que
    muere. Luego busca otra victima y asi sucesivamente"""
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        super().__init__(id, consume, reserves, conn, movement, attack_range)
        self.color = (255, 0, 0)  # Red
        self.current_victim = None
        self.current_victim_position = None
        self.current_victim_sugar = None

    def __distance_to_current_victim__(self, movement : Tuple[int, int]) -> Tuple[int, int]:
        """Dado un movimiento, devuelve una tupla con la distancia de la posicion a la que se
        llegara a la posicion de la victima actual como primer componente. Como segundo
        componente devolvera la cantidad de azucar en la casilla a la que se llegara multiplicada
        por -1. De esta manera la casilla para el mejor movimiento sera la tupla con el menor valor"""
        new_position = (self.position[0] + movement[0], self.position[1] + movement[1])
        if movement == (0, 0):
            sugar = 0
        else:
            try:
                sugar = self.geographic_memory.get_last_info_of_sugar_in_position(new_position[0], new_position[1])[1]
            except:
                sugar = 0
        if not self.current_victim:
            return (0, -sugar)
        return (CombatantAgent.__distance__(new_position, self.current_victim_position), -sugar)

    def __distance__(positionA : Tuple[int, int], positionB : Tuple[int, int]):
        return abs(positionA[0] - positionB[0]) + abs(positionA[1] - positionB[1])

    def __find_victim__(self):
        """Selecciona al agente mas cercano y que tenga menos azucar como victima"""
        try:
            return min([(CombatantAgent.__distance__(victim_position, self.position), resources, victim_id) for victim_id, (victim_position, iteration, resources) in self.memory_for_agents_sights.get_last_observation_of_each_agent().items() if (victim_id not in self.allys)])[2]
        except:
            return None
        
    def move(self):
        """Se mueve hacia donde se encuentre su current_victim y en caso de que esta haya muerto,
        se mueve hacia donde pueda comenzar un ataque lo mas pronto posible y asi tener una
        nueva victima"""
        if self.current_victim:
            if self.current_victim in self.memory_for_attacks.deaths:
                self.current_victim = None
                self.current_victim_position = None
                self.current_victim_sugar = None
            else:
                self.current_victim_position, iteration, self.current_victim_sugar = self.memory_for_agents_sights.get_last_info_from_agent(self.current_victim)
                #if self.current_victim_sugar > self.reserves:
                #    #si la victima esta mas fuerte que nosotros la dejamos tranquila
                #    self.current_victim = None
                #    self.current_victim_position = None
                #    self.current_victim_sugar = None
        
        possible_moves = self.movement.pure_moves()
        if not self.current_victim:
            self.current_victim = self.__find_victim__()
            if self.current_victim:
                self.current_victim_position, _, self.current_victim_sugar = self.memory_for_agents_sights.get_last_info_from_agent(self.current_victim)
        return min(possible_moves, key= self.__distance_to_current_victim__)


    def inform_move(self, movement: Tuple[int, int]):
        super().inform_move(movement)

    def inform_position(self, position: Tuple[int, int] = None):
        pass

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_received: Tuple[int, int]
    ):
        super().inform_of_attack_received(attacker_id, strength)

    def get_attacks(self) -> List[Action]:
        if not self.current_victim:
            return []
        return [Attack(self.id, self.current_victim, int(min(self.reserves/2, self.current_victim_sugar)))]

    def get_association_proposals(self) -> List:
        return []

    def inform_joined_association(
        self,
        association_id: int,
        members: List[int],
        commitments: Dict[int, Tuple[int]],
    ):
        super().inform_joined_association(association_id, members, commitments)

    def inform_broken_association(self, association_id: int):
        super().inform_broken_association(association_id)

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        return False

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        super().inform_of_attack_made(victim_id, strength)

    def take_attack_reward(self, victim_id: int, reward: int):
        super().take_attack_reward(victim_id, reward)

    def see_objects(self, info: List[Object_Info]):
        super().see_objects(info)

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        super().see_resources(info)

    def see_actions(self, info: List[Action_Info]):
        super().see_actions(info)

    def feed(self, sugar: int) -> None:
        super().feed(sugar)

    def burn(self) -> None:
        super().burn()