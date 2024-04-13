from abc import ABC, abstractmethod
from typing import Tuple, List
from environment.object_info import Object_Info

class IAgent(ABC):
    @abstractmethod
    def move(self, possible_destinations : List[Tuple[int, int]]) -> Tuple[int, int]:
        """Receives a list of possible destinations and returns the one where the player wants
        to move to"""
        pass
    
    def inform_move(self, position : Tuple[int, int]) -> None:
        "Informs the agent he has moved to the given position"
        pass

    @abstractmethod
    def see(self, info : List[Tuple[Tuple[int, int], Object_Info]]) -> None:
        "This method passes the agent the information about what he can see"
        pass