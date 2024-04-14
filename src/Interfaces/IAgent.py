from abc import ABC, abstractmethod
from typing import Tuple, List
from environment.sim_object import Object_Info
from environment.actions import Action_Info

class IAgent(ABC):
    @abstractmethod
    def move(self, possible_destinations : List[Tuple[int, int]]) -> Tuple[int, int]:
        """Dada una lista de movimientos posibles, descritos como tuplas
        (desplazamiento_horizontal, desplazamiento_vertical), devuelve una de tales tuplas
        el movimiento seleccionado a realizar"""
        pass
    
    @abstractmethod
    def inform_move(self, position : Tuple[int, int]) -> None:
        """Informa al agente sobre el desplazamiento que realizo (que puede no ser excactamente
        el que el deseaba)"""
        pass

    @abstractmethod
    def see_objects(self, info : List[Object_Info]) -> None:
        """Informa al agente de los objetos que puede ver"""
        pass

    @abstractmethod
    def see_resources(self, info : List[Tuple[Tuple[int, int], int]]) -> None:
        """Informa al agente acerca de la cantidad de azucar en las posiciones en su rango de 
        posicion"""
        pass

    @abstractmethod
    def see_actions(self, info : List[Action_Info]):
        "Informa al agente las acciones que ocurrieron en el pasado turno en su rango de vision"
        pass

    @abstractmethod
    def feed(self, sugar : int) -> None:
        """Informa al agente la cantidad de azucar que acaba de recolectar"""
        pass