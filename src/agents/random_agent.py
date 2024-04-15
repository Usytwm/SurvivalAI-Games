from typing import List, Tuple
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Attack
from Interfaces.IAgent import IAgent
from random import randint
class Random_Agent(IAgent):
    def move(self, possible_destinations: List[Tuple[int, int]]) -> Tuple[int, int]:
        return possible_destinations[randint(0, len(possible_destinations) - 1)]
    
    def inform_move(self, position: Tuple[int]) -> None:
        pass

    def get_actions(self, possible_victims : List[int]) -> List[Action]:
        if possible_victims:
            selected_victim = possible_victims[randint(0, len(possible_victims) - 1)]
            return [Attack(None, selected_victim, 1)]
        return []

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        print("He realizado un ataque a " + str(victim_id) + " con fuerza " + str(strength))

    def inform_of_received_attack(self, attacker_id: int, strength: int) -> None:
        print("He recibido un ataque de " + str(attacker_id) + " con fuerza " + str(strength))

    def take_attack_reward(self, victim_id: int, reward: int):
        print("He cobrado una recompensa de " + str(reward) + " por matar a " + str(victim_id))

    def see_objects(self, info: List[Object_Info]) -> None:
        for obj in info:
            print(str(obj.position) + " : " + str(obj.id))
        pass

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        pass

    def see_actions(self, info : List[Action_Info]):
        for action in info:
            print(str(action.type) + " in " + str(action.start_position))

    def feed(self, sugar: int) -> None:
        pass