import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/environment')
from typing import Tuple, Dict
from Interfaces.IAgent import IAgent
from Interfaces.IRange import IRange
from Interfaces.IBlurrier import IBlurrier
from map import Map
from sim_object import Sim_Object, Sim_Object_Type

class Agent_Handler(Sim_Object):
    def __init__(self, id : int, map : Map, agent : IAgent, movement_range : IRange, vision_range : IRange, blurrier : IBlurrier):
        super().__init__(id, Sim_Object_Type.AGENT)
        self.map = map
        self.agent = agent
        self.movement_range = movement_range
        self.vision_range = vision_range
        self.blurrier = blurrier
    
    def move(self) -> Tuple[int, int]:
        "Gets the position the agent wants to move to"
        possible_moves = [tpl[0] for tpl in self.movement_range.range(self.map, self.id)]
        return self.agent.move(possible_moves)
    
    def inform_move(self, position : Tuple[int, int]) -> None:
        "Informs the agent he has moved to the given position"
        return self.agent.inform_move(position)
    
    def see(self, objects : Dict[int, Sim_Object]) -> None:
        "Loads the sight of the agent in this turn, and sends it to him"
        vision = self.vision_range.range(self.map, self.id)
        position = self.map.peek_id(self.id)
        vision = self.blurrier.blurrify(self.id, position, vision, objects)
        self.agent.see(vision)