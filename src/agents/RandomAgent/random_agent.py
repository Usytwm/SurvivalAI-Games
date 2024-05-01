import sqlite3
from typing import Dict, List, Tuple
from agents.Agent_with_Memories import Agent_with_Memories
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Association_Proposal, Attack
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
import random

from typing import List, Tuple


class RandomAgent(Agent_with_Memories):
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        super().__init__(id, consume, reserves, conn, movement, attack_range)
        self.color = (255, 255, 0)  # yellowF

    def move(self):
        return self.movement.pure_moves()[random.randint(0, len(self.movement.pure_moves()) -1)]

    def get_attacks(self) -> List[Action]:
        """Para todo agente que estemos seguro se encuentra a nuestro alcance, decidimos si
        atacarlo o no lanzando una moneda al aire"""
        attacks = []
        for victim_id, (victim_position, iteration, victim_resources) in self.memory_for_agents_sights.get_last_observation_of_each_agent().items():
            if (iteration + 1 == self.iteration) and (self.attack_range.victim_within_range(self.position, victim_position)) and (random.random() < 0.5):
                strength = random.randint(0, self.reserves)
                attacks.append(Attack(self.id, victim_id, strength))
        return attacks

    def get_association_proposals(self) -> List:
        """Se asocia a una cantidad random de agentes"""
        num_of_associations = min(int(1/random.random()) - 1, 5)
        associations = []
        for i in range(0, num_of_associations):
            num_of_members = min(min((1 + int(1/random.random()), 5)), len(self.memory_for_agents_sights.agents_seen))
            seen_agents = list(self.memory_for_agents_sights.agents_seen.keys())
            members = random.sample(seen_agents, num_of_members - 1)
            members.append(self.id)
            commitments = {id : (0.2, 1/num_of_members) for id in members}
            associations.append(Association_Proposal(self.id, members, commitments))
        return associations

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        "Devuelve si el agente acepta ser parte de la asociacion o no"
        return random.random() < 0.25