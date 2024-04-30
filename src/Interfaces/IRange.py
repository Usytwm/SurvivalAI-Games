from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from environment.map import Map

class IRange(ABC):
    @abstractmethod
    def get_range(self, map : Map, id : int) -> List[Tuple[Tuple[int, int], Any]]:
        """Given an id and a map, returns all the positions that will be affected if the agent
        with such id, takes an action with this range.

        Returns a list of tuples of positions and an info related to such positions
        """
        pass

    @abstractmethod
    def within_range(self, start_position : Tuple[int, int], goal_position : Tuple[int, int]) -> bool:
        """Dada una posicion de partida y una posicion objetivo determina si esta ultima esta
        al alcance"""
        pass