from typing import List, Tuple
from environment.object_info import Object_Info
from Interfaces.IAgent import IAgent
from random import randint
class Random_Agent(IAgent):
    def move(self, possible_destinations: List[Tuple[int, int]]) -> Tuple[int, int]:
        return possible_destinations[randint(0, len(possible_destinations) - 1)]
    def inform_move(self, position: Tuple[int]) -> None:
        pass
    def see(self, info: List[Tuple[Tuple[int, int], Object_Info]]) -> None:
        for position, obj in info:
            print(str(position) + " : " + str(obj.id))
        pass