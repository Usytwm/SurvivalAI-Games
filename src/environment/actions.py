from typing import Tuple, NamedTuple
from enum import Enum

class ActionType(Enum):
    ATTACK = 1
    PLACE_TRAP = 2

class Action(NamedTuple):
    type : ActionType
    agent : str
    direction : Tuple[int, int] | None = None

class Alliance_Solicitude:
    pass