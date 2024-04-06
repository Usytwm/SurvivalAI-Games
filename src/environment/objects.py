from typing import Tuple, NamedTuple, List
from enum import Enum
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
    def __init__(self):
        self.id = " "
    def __eq__(self, other):
        return self.id == other.id

class Empty(Object_Info):
    pass

class Presence(Object_Info):
    def __init__(self):
        self.id = "X"

class Agent_Image(Object_Info):
    """Representa la imagen que se forma un agente de otro agente cuando lo ve a lo
    lejos. Mientras mas cercano, mas informacion, mientras mas lejos, mas campos nulos"""
    def __init__(self, id = None, ammo = None, health = None):
        self.id = id
        self.ammo = ammo
        self.health = health