import sqlite3
from typing import List, Tuple, Dict
from Interfaces.IAgent import IAgent
from agents.random_agent import Random_Agent
from environment.actions import Action_Info, Attack
from environment.sim_object import Object_Info, Agent_Info
from environment.actions import Action_Type
from agents.memory.memory_for_agents_sights import Memory_for_Agents_Sights
from agents.memory.geographic_memory import Geographic_Memory
from agents.memory.memory_for_attacks import Memory_for_Attacks
class Agent_with_Memories(Random_Agent):
    def __init__(self, id : int, consume : int, reserves, conn : sqlite3.Connection):
        self.id = id
        self.consume = consume
        self.reserves = reserves
        self.position = (0, 0)
        self.iteration = 0
        self.geographic_memory = Geographic_Memory(id)
        self.memory_for_agents_sights = Memory_for_Agents_Sights(id, conn)
        self.memory_for_attacks = Memory_for_Attacks(id, conn)
        self.own_moves : Dict[int, Tuple[int, int]] = {}
        self.positions_visited : Dict[int, Tuple[int, int]] = {}
        self.attacks_made : Dict[int, Tuple[int, int]] = {}
        self.attacks_received : Dict[int, Tuple[int, int]] = {}
    
    #En IAgent deberiamos cambiar el nombre del parametro position por movement
    def inform_move(self, position: Tuple[int, int]) -> None:
        self.own_moves[self.iteration] = position
        self.position = (self.position[0] + position[0], self.position[1] + position[1])
        self.positions_visited[self.iteration] = self.position

    def see_objects(self, info: List[Object_Info]) -> None:
        for sight in info:
            if isinstance(sight, Agent_Info):
                other_id = sight.id
                row = sight.position[0] + self.position[0]
                column = sight.position[1] + self.position[1]
                resources = sight.resources
            self.memory_for_agents_sights.add_appearence(other_id, row, column, self.iteration, resources)
            self.geographic_memory.add_position(row, column)
        self.iteration = self.iteration + 1
    
    def see_resources(self, info: List[Tuple[Tuple[int] | int]]) -> None:
        for (row, column), sugar in info:
            row = row + self.position[0]
            column = column + self.position[1]
            self.geographic_memory.add_sugar_observation(row, column, self.iteration, sugar)
    
    def see_actions(self, info: List[Action_Info]):
        for action in info:
            match action.type:
                case Action_Type.DIE:
                    self.memory_for_attacks.add_death(action.actor_id, self.iteration)
                case Action_Type.ATTACK:
                    self.memory_for_attacks.add_attack(action.actor_id, action.destinataries_ids[0], self.iteration, action.strength)
                case Action_Type.ASSOCIATION_CREATION:
                    pass
    
    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        if not self.iteration in self.attacks_made:
            self.attacks_made[self.iteration] = []
        self.attacks_made[self.iteration].append((victim_id, strength))
    
    def inform_of_attack_received(self, attacker_id: int, strength: int, position_attack_recived: Tuple[int]) -> None:
        if not self.iteration in self.attacks_received:
            self.attacks_received[self.iteration] = []
        self.attacks_received[self.iteration].append((attacker_id, strength))
    
    def burn(self) -> None:
        self.reserves = self.reserves - self.consume
    
    def feed(self, sugar: int) -> None:
        self.reserves = self.reserves + sugar
    
    def take_attack_reward(self, victim_id: int, reward: int):
        self.reserves = self.reserves + reward
        self.memory_for_attacks.add_death(victim_id, self.iteration)
    
    def inform_position(self, position: Tuple[int]) -> None:
        #Por ahora
        pass