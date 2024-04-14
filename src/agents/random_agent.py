from typing import List, Tuple
from environment.sim_object import Object_Info
from environment.actions import Action_Info
from Interfaces.IAgent import IAgent
from random import randint
class Random_Agent(IAgent):
    def move(self, possible_destinations: List[Tuple[int, int]]) -> Tuple[int, int]:
        return possible_destinations[randint(0, len(possible_destinations) - 1)]
    def inform_move(self, position: Tuple[int]) -> None:
        pass
    def see_objects(self, info: List[Object_Info]) -> None:
        for obj in info:
            print(str(obj.position) + " : " + str(obj.id))
        pass
    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        pass
    def see_actions(self, info : List[Action_Info]):
        for action in info:
            print(str(action.type.name) + " in " + str(action.start_position))
    def feed(self, sugar: int) -> None:
        pass