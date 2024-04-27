from random import random
from typing import List, Tuple
from Interfaces.IAgent import IAgent
from environment.actions import Action, Action_Info, Attack
from environment.sim_object import Object_Info


class DiplomatAgent(IAgent):
    def __init__(self, id):
        self.id = id

    def move(self, possible_moves) -> Tuple[int, int]:
        """Decide el siguiente movimiento basado en el recurso más cercano y rico en azúcar."""
        return (0, 0)

    def inform_move(self, movement: Tuple[int, int]):
        self.position = movement
        print(f"Se ha movido a la posición {movement}")

    def inform_position(
        self, position: Tuple[int] = None, reserve: int = None, health: int = None
    ) -> None:
        if position:
            self.position = position
        if reserve:
            self.reserve = reserve
        if health:
            self.health = health

    def get_attacks(self) -> List[Action]:
        attacks = []
        for i in range(1, 2):
            if random() < 0.5:
                attacks.append(Attack(self.id, i, 1))
        return attacks
        # if randint(0, 100) < 20:  # 20% chance to attack
        #     target_id = randint(1, 10)  # Random target for example
        #     return [Attack(self.id, target_id, 1)]
        # return []

    def get_association_proposals(self) -> List:
        return []

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        print(f"Attack made on agent {victim_id} with strength {strength}")

    def inform_of_received_attack(self, attacker_id: int, strength: int) -> None:
        print(f"Received attack from agent {attacker_id} with strength {strength}")

    def take_attack_reward(self, victim_id: int, reward: int):
        print(f"Received reward of {reward} for defeating agent {victim_id}")

    def see_objects(self, info: List[Object_Info]) -> None:
        self.current_see_objects = info
        print(f"Seeing objects: {info}")

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        self.current_see_resources = info
        print(f"Seeing resources: {info}")

    def see_actions(self, info: List[Action_Info]):
        self.current_see_actions = info
        print(f"Actions seen: {info}")

    def feed(self, sugar: int) -> None:
        print(f"Received {sugar} units of sugar")

    def burn(self) -> None:
        print("Consuming daily ration of sugar")
