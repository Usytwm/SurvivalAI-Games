from typing import List
from Interfaces.IAgent import IAgent
from environment.actions import Action, ActionType
from random import randint

class Random_Agent(IAgent):
    def __init__(self):
        pass
    def move(self):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        return directions[randint(0, 3)]
    def actions(self) -> List[Action]:
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        direction = directions[randint(0, 3)]
        return [Action(ActionType.ATTACK, None, direction)]
    def actualize_personal_info(self) -> None:
        pass
    def falled_in_a_trap(self) -> None:
        pass
    def received_attack(self) -> None:
        pass
    def view(self, sight: List) -> None:
        pass