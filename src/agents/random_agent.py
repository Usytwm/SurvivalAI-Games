from typing import List, Tuple, Dict
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Association_Proposal, Attack
from Interfaces.IAgent import IAgent
from random import randint, random


class Random_Agent(IAgent):
    def __init__(self, id):
        self.id = id

    def move(self) -> Tuple[int, int]:
        directions = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
        return directions[randint(0, 4)]

    def inform_move(self, movement: Tuple[int]) -> None:
        pass

    def get_attacks(self) -> List[Action]:
        attacks = []
        for i in range(1, 5):
            if random() < 0.5:
                attacks.append(Attack(self.id, i, 1))
        return attacks

    def get_association_proposals(self) -> List:
        if self.id != 2:
            commitments = {}
            commitments[self.id] = (0.2, 0.5)
            commitments[2] = (0.2, 0.5)
            proposal = Association_Proposal(self.id, randint(1, 1000000), [self.id, 2], commitments)
            return [proposal]
        else:
            return []
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        #por ahora
        return True

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        print(
            f"{self.id} ha realizado un ataque a "
            + str(victim_id)
            + " con fuerza "
            + str(strength)
        )

    def inform_of_attack_received(self, attacker_id: int, strength: int) -> None:
        print(
            f"{self.id} ha recibido un ataque de "
            + str(attacker_id)
            + " con fuerza "
            + str(strength)
        )
    
    def inform_joined_association(self, association_id: int, members: List[int], commitments: Dict[int, Tuple[int]]):
        pass

    def inform_broken_association(self, association_id: int):
        pass

    def take_attack_reward(self, victim_id: int, reward: int):
        print(
            "He cobrado una recompensa de "
            + str(reward)
            + " por matar a "
            + str(victim_id)
        )

    def see_objects(self, info: List[Object_Info]) -> None:
        for obj in info:
            print(str(obj.position) + " : " + str(obj.id))
        pass

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        pass

    def see_actions(self, info: List[Action_Info]):
        for action in info:
            print(str(action.type) + " in " + str(action.start_position))

        print("End of actions")

    def feed(self, sugar: int) -> None:
        pass

    def burn(self) -> None:
        pass
