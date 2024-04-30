import sqlite3
from typing import Dict, List, Tuple
from agents.Agent_with_Memories import Agent_with_Memories
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Association_Proposal, Attack
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
from random import randint, random

from typing import List, Tuple


class RandomAgent(Agent_with_Memories):
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        super().__init__(id, consume, reserves, conn, movement, attack_range)
        self.color = (255, 255, 0)  # yellowF

    def move(self):
        return self.movement.pure_moves()[randint(0, len(self.movement.pure_moves()) -1)]

    def inform_move(self, movement: Tuple[int, int]):
        super().inform_move(movement)

    def inform_position(self, position: Tuple[int, int] = None):
        pass

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_received: Tuple[int, int]
    ):
        super().inform_of_attack_received(attacker_id, strength)

    def get_attacks(self) -> List[Action]:
        """Para todo agente que estemos seguro se encuentra a nuestro alcance, decidimos si
        atacarlo o no lanzando una moneda al aire"""
        attacks = []
        for victim_id, (victim_position, iteration, victim_resources) in self.memory_for_agents_sights.get_last_observation_of_each_agent().items():
            if (iteration + 1 == self.iteration) and (self.attack_range.victim_within_range(self.position, victim_position)) and (random() < 0.5):
                strength = randint(0, self.reserves)
                attacks.append(Attack(self.id, victim_id, strength))
        return attacks

    def get_association_proposals(self) -> List:
        return []
        decision = self.estrategy.make_decision()
        filtered = list(
            filter(lambda x: x.key == Knowledge.GETASSOCIATIONPROPOSALS, decision)
        )
        if len(filtered) == 0:
            return []
        association_Proposal = list(map(lambda x: x.data, filtered))[0]
        return association_Proposal

    def inform_joined_association(self, association_id: int, members: List[int], commitments: Dict[int, Tuple[int]]):
        super().inform_joined_association(association_id, members, commitments)

    def inform_broken_association(self, association_id: int):
        super().inform_broken_association(association_id)

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        "Devuelve si el agente acepta ser parte de la asociacion o no"
        return random() < 0.25

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