from typing import Any, Dict, List, Tuple
from Interfaces.IBlurrier import IBlurrier
from environment.object_info import Object_Info
from environment.sim_object import Sim_Object, Sim_Object_Type
from environment.object_info import Agent_Info
"""De cada objeto vemos su id y su tipo, no importa su distancia"""
class Simple_Blurrier(IBlurrier):
    def blurrify(self, id: int, position: Tuple[int, int], vision: List[Tuple[Tuple[int, int], int]], objects_dict: Dict[int, Sim_Object]) -> List[Tuple[Tuple[int, int], Object_Info]]:
        processed_sight = []
        for position, id in vision:
            if not id:
                continue
            obj = objects_dict[id]
            match obj.type:
                case Sim_Object_Type.AGENT:
                    obj = Agent_Info(obj.id, obj.type)
            processed_sight.append((position, obj))
        return processed_sight