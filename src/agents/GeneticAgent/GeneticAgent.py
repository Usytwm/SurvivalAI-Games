from random import random
import sqlite3
from typing import Dict, List, Tuple
from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info, Association_Proposal, Attack
from environment.sim_object import Object_Info
#from agents.GenetictAgent.Rules import (
#    eat_not_agents_rule,
#    attack_enemy_in_vision,
#    attack_not_enemy_in_vision,
#    move_not_enemy,
#    recived_attacker,
#    default_move,
#    association_proposal_rule,
#    recived_association_proposal_rule,
#)


class GenetictAgent(Agent_with_Memories):
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection):
        super().__init__(id, consume, reserves, conn)
        self.color = (255, 0, 0)  # Red
        initial_facts = [
            Fact(Knowledge.ALLIES, set()),
            Fact(Knowledge.ENEMIES, set()),
            Fact(Knowledge.AGEENTS, set()),
            Fact(Knowledge.NEXT_MOVE, (0, 0)),
            Fact(Knowledge.ID, id),
            Fact(Knowledge.RESERVE, reserves),
            Fact(Knowledge.GEOGRAPHIC_MEMORY, self.geographic_memory),
            Fact(Knowledge.MEMORY_FOR_AGENTS_SIGHTS, self.memory_for_agents_sights),
            Fact(Knowledge.MEMORY_FOR_ATTACKS, self.memory_for_attacks),
            Fact(Knowledge.ASSOCIATION, self.associations),
            Fact(Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, False),
        ]
        initial_rules = [
            eat_not_agents_rule,
            attack_enemy_in_vision,
            attack_not_enemy_in_vision,
            move_not_enemy,
            recived_attacker,
            default_move,
            association_proposal_rule,
            recived_association_proposal_rule,
        ]

        self.estrategy = Estrategy(initial_facts, initial_rules)

    def move(self, possible_moves: List[Tuple[int, int]]):
        self.estrategy.learn_especific(Knowledge.POSIBLES_MOVEMENTS, possible_moves)
        # Solicitar una decisión de movimiento
        decision = self.estrategy.make_decision()
        filter_desicion = list(filter(lambda x: x.key == Knowledge.NEXT_MOVE, decision))
        move = list(
            map(
                lambda x: x.data,
                filter_desicion,
            )
        )[0]
        position = self.estrategy.get_knowledge(Knowledge.POSITION)
        self.estrategy.learn_especific(Knowledge.PREVPOSSITION, position)
        return move

    def inform_move(self, movement: Tuple[int, int]):
        super().inform_move(movement)
        self.estrategy.learn_especific(Knowledge.POSITION, movement)

    def inform_position(self, position: Tuple[int, int] = None):
        if position:
            self.position = position
            self.estrategy.learn_especific(Knowledge.POSITION, position)

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_received: Tuple[int, int]
    ):
        super().inform_of_attack_received(attacker_id, strength)
        # Cuando se recibe un ataque, actualizar los hechos y solicitar una decisión
        self.estrategy.learn_especific(
            Knowledge.RECEIVED_ATTACK,
            (
                attacker_id,
                strength,
                position_attack_received,
            ),
        )
        enemy = self.estrategy.get_knowledge(Knowledge.ENEMIES)
        enemy.add(attacker_id)
        self.estrategy.learn_especific(Knowledge.ENEMIES, enemy)

    def get_attacks(self) -> List[Action]:
        decision = self.estrategy.make_decision()
        filtered = list(filter(lambda x: x.key == Knowledge.GETATTACKS, decision))
        if len(filtered) == 0:
            return []
        attacks = list(map(lambda x: x.data, filtered))[0]
        return attacks

    def get_association_proposals(self) -> List:
        decision = self.estrategy.make_decision()
        filtered = list(
            filter(lambda x: x.key == Knowledge.GETASSOCIATIONPROPOSALS, decision)
        )
        if len(filtered) == 0:
            return []
        association_Proposal = list(map(lambda x: x.data, filtered))[0]
        return association_Proposal

    def inform_joined_association(
        self,
        association_id: int,
        members: List[int],
        commitments: Dict[int, Tuple[int]],
    ):
        super().inform_joined_association(association_id, members, commitments)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION, self.associations)

    def inform_broken_association(self, association_id: int):
        super().inform_broken_association(association_id)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION, self.associations)

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        super().consider_association_proposal(proposal)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION_PROPOSALS, proposal)
        desicion = self.estrategy.make_decision()
        filtered = list(
            filter(lambda x: x.key == Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, desicion)
        )
        self.estrategy.remove_knowledge(Knowledge.ASSOCIATION_PROPOSALS)
        if len(filtered) == 0:
            return False
        return list(map(lambda x: x.data, filtered))[0]

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        super().inform_of_attack_made(victim_id, strength)

    def take_attack_reward(self, victim_id: int, reward: int):
        super().take_attack_reward(victim_id, reward)
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)

    def see_objects(self, info: List[Object_Info]):
        super().see_objects(info)
        # Actualizar la base de hechos con la información de objetos vistos
        self.estrategy.learn_especific(Knowledge.SEE_OBJECTS, info)

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        super().see_resources(info)
        self.estrategy.learn_especific(Knowledge.SEE_RESOURCES, info)

    def see_actions(self, info: List[Action_Info]):
        super().see_actions(info)
        # Actualizar la base de hechos con acciones vistas
        self.estrategy.learn_especific(Knowledge.SEE_ACTIONS, info)

    def feed(self, sugar: int) -> None:
        super().feed(sugar)
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)

    def burn(self) -> None:
        super().burn()
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)
