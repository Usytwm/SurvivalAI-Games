from abc import ABC, abstractmethod
from environment.map import Map
from typing import List, Tuple

class IAttackRange(ABC):
    def possible_victims(self, map : Map, id : int) -> List[int]:
        """Dado un mapa y un agente, este metodo devuelve la lista con los id de todos los 
        agentes que pueden ser atacados por el agente con el id provisto"""
        pass

    def victim_within_range(self, actual_position : int, victim_position : int) -> bool:
        """Dada la posicion actual y la posicion de una victima determina si esa es alcanzable
        por un ataque iniciado en esta posicion"""
        pass