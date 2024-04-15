from enum import Enum
from typing import List, Tuple

class Action_Type(Enum):
    DIE = 1
    ATTACK = 2

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