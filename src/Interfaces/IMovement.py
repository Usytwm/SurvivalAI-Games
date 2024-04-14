from abc import ABC, abstractmethod
from environment.map import Map
from typing import List, Tuple

class IMovement(ABC):
    def moves(self, map : Map, id : int) -> List[Tuple[int, int]]:
        """Devuelve todos los posibles movimientos que puede realizar el agente con el id
        provisto en el tablero provisto. Retorna una lista de tuplas, donde cada elemento 
        describe un movimiento como el desplazamiento vertical y horizontal que realizara
        el agente\n
        Por ejemplo si el agente se mueve dos filas hacia arriba el movimiento seria
        representado con la tupla (2, 0)
        """
        pass