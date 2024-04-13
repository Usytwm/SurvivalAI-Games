from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from environment.sim_object import Sim_Object
from environment.object_info import Object_Info
class IBlurrier(ABC):
    def blurrify(self, id : int, position : Tuple[int, int], vision : List[Tuple[Tuple[int, int], int]], objects_dict : Dict[int, Sim_Object]) -> List[Tuple[Tuple[int, int], Object_Info]]:
        """This method prepares the info the agent can see of an object. The visualization
        method provided by IRange just says the id and the ubication of the objects within
        range of sight. This method will, for the closer objects, provide more info to the
        agent about what he is seen, like the health of the other agent or his ammo, or the
        detail we want. Likewise, this method will blurry information about the furthest
        objects, so the agent can just see that there is somethong there, a presence, without
        exactly knowing what or who is it\n
        For this purpose, takes the following input:
        -The id of the agent who's sight we are preparing
        -The position of such agent
        -The output of the IRange method for vision, that is List[Tuple[Tuple[int, int], int]]
        -The Sim dictionary that corresponds every id to an object
        """
        pass