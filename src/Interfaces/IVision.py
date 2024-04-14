from abc import ABC, abstractmethod
from environment.map import Map
from environment.sim_object import Sim_Object, Object_Info
from environment.actions import Action_Info
from typing import Dict, List, Tuple

class IVision(ABC):
    @abstractmethod
    def see_objects(map : Map, id : int, objects : Dict[int, Sim_Object]) -> List[Object_Info]:
        """Dado un mapa, un id y un diccionario que contiene todos los objetos de la simulacion
        accesibles a traves de su id; este metodo prepara la vista de los objetos que tiene el
        agente con el id provisto.\n
        El valor de retorno sera una lista de Object_Info clase que describe al objeto
        (incluida su posicion relativa al agente)"""
        pass

    @abstractmethod
    def see_resources(self, map : Map, id : int) -> List[Tuple[Tuple[int, int], int]]:
        """Dado un mapa y un id, devuelve una lista con cada posicion que el agente con el id
        provisto puede apreciar desde su posicion\n
        El valor de retorno sera una lista de tuplas (position, cant_sugar), donde la posicion
        se refiere a la posicion relativa con respeto al usuario y la cant_sugar es un entero\n
        Por ejemplo si hay 3 de azucar, 2 posiciones a la izquierda del agente, la tupla
        ((0, 2), 3) seria la representacion de tal observacion"""
        pass

    @abstractmethod
    def see_actions(self, map : Map, id : int) -> List[Action_Info]:
        """Dado un mapa y un id, devuelve una lista de las acciones que han ocurrido en el rango
        de vision del agente con el id provisto"""
        pass