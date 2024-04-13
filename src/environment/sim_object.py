from enum import Enum
class Sim_Object_Type(Enum):
    AGENT = 1

class Sim_Object:
    def __init__(self, id : int, type : Sim_Object_Type):
        self.id = id
        self.type = type