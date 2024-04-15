from abc import ABC, abstractmethod
from environment.map import Map
from typing import List, Tuple

class IAttackRange(ABC):
    def possible_victims(self, map : Map, id : int) -> List[int]:
        """Dado un mapa y un agente, este metodo devuelve la lista con los id de todos los 
        agentes que pueden ser atacados por el agente con el id provisto"""
        pass