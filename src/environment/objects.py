from typing import Tuple, NamedTuple, List
from enum import Enum
from Interfaces.IAgent import IAgent
class Object_Type(Enum):
    Agent = 1
    Obstacle = 2
    Ammo = 3
    Weapon = 4
    Trap = 5

class Sim_Object:
    def __init__(self, id_number, type : Object_Type):
        #self.id = type.name + str(id_number)
        self.id = str(id_number)
        self.type = type

class Object_Info:
    pass