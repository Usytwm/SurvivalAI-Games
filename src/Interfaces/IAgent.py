from abc import ABC, abstractmethod
from typing import Tuple, List, Dict
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Attack, Association_Proposal


class IAgent(ABC):

    @abstractmethod
    def move(self, possible_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Devuelve el movimiento que desea realizar el agente este turno. El movimiento es
        expresado como una tupla que representa el movimiento en la posicion horizontal y en la
        vertical respectivamente, por ejemplo (-1, 3) representa que se movio una fila hacia
        arriba y tres columnas a la derecha"""
        pass

    @abstractmethod
    def get_attacks(self) -> List[Attack]:
        """Devuelve una lista con los ataques que el agente desea realizar este turno"""
        pass

    @abstractmethod
    def get_association_proposals(self) -> List[Association_Proposal]:
        """Devuelve una lista con las propuestas de Asociacion que el agente desea realizar este
        turno"""
        pass

    @abstractmethod
    def consider_association_proposal(self, proposal : Association_Proposal) -> bool:
        "Devuelve si el agente acepta ser parte de la asociacion o no"
        pass
    
    @abstractmethod
    def inform_joined_association(self, association_id : int, members : List[int], commitments : Dict[int, Tuple[int, int]]):
        "Informa al agente que se acaba de unir a una asociacion"
        pass

    @abstractmethod
    def inform_broken_association(self, association_id : int):
        "Informa al agente que se acaba de diluir una asociacion a la que pertenece"

    @abstractmethod
    def inform_move(self, movement: Tuple[int, int]) -> None:
        """Informa al agente sobre el desplazamiento que realizo (que puede no ser excactamente
        el que el deseaba)"""
        pass

    @abstractmethod
    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        "Informa al agente que un ataque que solicito, ha sido ejecutado"
        # O sea, si la solicitud del agente estaba mal formulada no le llegara esta confirmacion
        # luego, se dara cuenta de su error
        pass

    @abstractmethod
    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_recived: Tuple[int, int]
    ) -> None:
        "Informa al agente de un ataque recibido"
        pass

    @abstractmethod
    def take_attack_reward(self, victim_id: int, reward: int):
        "Informa al agente de la recompensa que le corresponde tras matar a un agente"
        # return self.agent.take_attack_reward(victim_id, reward)
        pass

    @abstractmethod
    def inform_position(self, position: Tuple[int, int]) -> None:
        """Informa al agente de su posicion actual"""
        pass

    @abstractmethod
    def see_objects(self, info: List[Object_Info]) -> None:
        """Informa al agente de los objetos que puede ver"""
        pass

    @abstractmethod
    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        """Informa al agente acerca de la cantidad de azucar en las posiciones en su rango de
        posicion"""
        pass

    @abstractmethod
    def see_actions(self, info: List[Action_Info]):
        "Informa al agente las acciones que ocurrieron en el pasado turno en su rango de vision"
        pass

    @abstractmethod
    def feed(self, sugar: int) -> None:
        """Informa al agente la cantidad de azucar que acaba de recolectar"""
        pass

    @abstractmethod
    def burn(self) -> None:
        """Informa al agente que acaba de consumir su racion diaria de azucar"""
        pass
