from enum import Enum
from typing import Tuple

class Sim_Object_Type(Enum):
    AGENT = 1

class Sim_Object:
    def __init__(self, id : int, type : Sim_Object_Type):
        self.id = id
        self.type = type

class Object_Info:
    def __init__(self, position : Tuple[int, int], id : int, type : Sim_Object_Type):
        self.position = position
        self.id = id
        self.type = type

class Agent_Info(Object_Info):
    pass