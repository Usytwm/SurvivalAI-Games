from enum import Enum
from typing import List, Tuple

class Action_Type(Enum):
    DIE = 1

class Action:
    def __init__(self, type : Action_Type, actor_id : int, victim_ids : List[int] = None):
        self.type = type
        self.actor_id = actor_id
        self.victim_ids = victim_ids

class Action_Info:
    def __init__(self, start_position : Tuple[int, int], type : Action_Type, actor_id : int = None, victim_ids : List[int] = None):
        self.start_position = start_position
        self.type = type
        self.actor_id = actor_id
        self.victim_ids = victim_ids