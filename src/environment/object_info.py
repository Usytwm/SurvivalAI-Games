from sim_object import Sim_Object_Type
class Object_Info:
    def __init__(self, id : int, type : Sim_Object_Type):
        self.id = id
        self.type = type

class Agent_Info(Object_Info):
    pass