from abc import ABC, abstractmethod
from typing import Tuple, List
from environment.actions import Action, Alliance_Solicitude
#from environment.objects import Object_Info

class IAgent(ABC):
    @abstractmethod
    def move(self) -> Tuple[int, int]:
        "Obtener un movimiento de parte del agente"
        pass

    @abstractmethod
    def actions(self) -> List[Action]:
        "Obtener una lista de las acciones que realizara el agente durante el turno"
        pass

    @abstractmethod
    def actualize_personal_info(self) -> None:
        "Recibe una actualizacion de los datos personales del agente"
        pass

    @abstractmethod
    def falled_in_a_trap(self) -> None:
        "Informa al agente that que ha caido en una trampa"
        pass

    @abstractmethod
    def received_attack(self) -> None:
        "Informa al agente que ha recibido un ataque"
        pass

    @abstractmethod
    def view(self, sight : List) -> None:
        "Muestra al agente la vista que le corresponde"
        pass