"""
from typing import List, Tuple, Dict
from Interfaces.IAgent import IAgent
from environment.actions import Action, ActionType
from environment.map_controller import Map
from environment.objects import Object_Info, Presence, Empty
from random import randint
from agents.random_agent import Random_Agent

class Agent_With_Vision(Random_Agent):
    def __init__(self, width_of_map, height_of_map):
        self.map = Map(width_of_map, height_of_map)
        self.id_to_position_dict : Dict[str, Tuple[int, int]] = {}
        self.id_to_object_info_dict : Dict[str, Object_Info] = {}
    
    def view(self, sight: List[Tuple[int, int, Object_Info]]) -> None:

        for x, y, obj in sight:
            if self.map.cell_content(x, y) == obj.id:
                continue
            self.__erase(x, y)
            self.__add(x, y, obj)
        print("El nuevo mapa interno para el agente es:")
        self.map.display()
        print("Fin de la presentacion")
    
    def __erase(self, x : int, y : int):
        old_content = self.map.cell_content(x, y)
        if old_content:
            self.map.remove_object(x, y)
            if old_content in ["X", " "]:
                return
            self.id_to_position_dict.pop(old_content)
            self.id_to_object_info_dict.pop(old_content)
    
    def __add(self, x : int, y : int, obj : Object_Info):
        self.map.add_object(x, y, obj.id)
        self.id_to_position_dict[obj.id] = (x, y)
        self.id_to_object_info_dict[obj.id] = obj
"""