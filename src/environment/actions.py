from enum import Enum
from typing import List, Tuple, Dict

class Action_Type(Enum):
    DIE = 1
    ATTACK = 2
    ASSOCIATION_PROPOSAL = 3
    ASSOCIATION_CREATION = 4

class Action:
    def __init__(self, type : Action_Type, actor_id : int, destinataries_ids : List[int] = None):
        self.type = type
        self.actor_id = actor_id
        self.destinataries_ids = destinataries_ids

class Attack(Action):
    def __init__(self, actor_id : int, destinatary_id : int, strength : int):
        super().__init__(self, Action_Type.ATTACK, [destinatary_id])
        self.type = Action_Type.ATTACK
        self.strength = strength

class Action_Info:
    def __init__(self, start_position : Tuple[int, int], type : Action_Type, actor_id : int = None, destinataries_ids : List[int] = None):
        self.start_position = start_position
        self.type = type
        self.actor_id = actor_id
        self.destinataries_ids = destinataries_ids

class Association_Proposal(Action):
    def __init__(self, actor_id : int, association_id : int, members : List[int], commitments : Dict[int, Tuple[int, int]]):
        super().__init__(Action_Type.ASSOCIATION_PROPOSAL, actor_id, members)
        self.association_id = association_id
        self.members = members
        self.commitments = commitments
    
class Association_Creation(Action):
    def __init__(self, actor_id : int, association_id : int, members : List[int], commitments : Dict[int, Tuple[int, int]]):
        #Realmente deberian ser conocidos los commitments por agentes ajenos a la asociacion
        super().__init__(Action_Type.ASSOCIATION_CREATION, actor_id, None)
        self.association_id = association_id
        self.members = members
        self.commitments = commitments