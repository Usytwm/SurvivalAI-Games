from typing import Tuple, NamedTuple
from enum import Enum

class ActionType(Enum):
    ATTACK = 1
    PLACE_TRAP = 2

class Action(NamedTuple):
    type : ActionType
    agent : str
    direction : Tuple[int, int] | None = None
    intensity : int = 1

class Alliance_Solicitude:
    pass