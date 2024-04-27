from enum import Enum
from typing import Tuple


class Sim_Object_Type(Enum):
    AGENT = 1


class Sim_Object:
    def __init__(self, id: int, type: Sim_Object_Type, resources : int):
        self.id = id
        self.type = type
        self.resources = resources

class Object_Info:
    def __init__(self, position: Tuple[int, int], id: int, type: Sim_Object_Type):
        self.position = position
        self.id = id
        self.type = type

    def __str__(self) -> str:
        return (
            f"ID:{str(self.id)}, Position:{str(self.position)}, Type:{str(self.type)}  "
        )

    def __repr__(self) -> str:
        return (
            f"ID:{str(self.id)}, Position:{str(self.position)}, Type:{str(self.type)}  "
        )

class Agent_Info(Object_Info):
    def __init__(self, position: Tuple[int, int], id : int, sugar : int):
        self.position = position
        self.resources = sugar
        self.id = id
        self.type = Sim_Object_Type.AGENT