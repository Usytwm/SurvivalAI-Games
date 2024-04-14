import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/environment')
from typing import Tuple, Dict
from Interfaces.IAgent import IAgent
from Interfaces.IRange import IRange
from Interfaces.IMovement import IMovement
from Interfaces.IVision import IVision
from map import Map
from sim_object import Sim_Object, Sim_Object_Type

class Agent_Handler(Sim_Object):
    def __init__(self, id : int, reserve : int, consume : int, map : Map, agent : IAgent, movement : IMovement, vision : IVision):
        super().__init__(id, Sim_Object_Type.AGENT)
        self.reserve = reserve
        self.consume = consume
        self.map = map
        self.agent = agent
        self.movement = movement
        self.vision = vision
    
    @property
    def IsDead(self):
        return (self.reserve < 0)
    
    def move(self) -> Tuple[int, int]:
        "Gets the position the agent wants to move to"
        possible_moves = self.movement.moves(self.map, self.id)
        return self.agent.move(possible_moves)
    
    def inform_move(self, position : Tuple[int, int]) -> None:
        "Informs the agent he has moved to the given position"
        return self.agent.inform_move(position)

    def see_objects(self, objects : Dict[int, Sim_Object]) -> None:
        "Loads the objects the agent can see in this turn, and sends it to him"
        vision = self.vision.see_objects(self.map, self.id, objects)
        self.agent.see_objects(vision)
    
    def see_resources(self) -> None:
        """Loads the info about the resources in the positions the agent can see in this turn
        and sends it to him"""
        #Solo puede ver cuanta azucar hay en las casillas que no estan ocupadas
        vision = self.vision.see_resources(self.map, self.id)
        self.agent.see_resources(vision)
    
    def see_actions(self) -> None:
        "Loads the info about events that had occured in the agents sight"
        vision = self.vision.see_events(self.map, self.id)
        self.agent.see_events(vision)

    def feed(self, sugar : int) -> None:
        """Increaes the agent reserves with the amount of sugar given, substracts the agent consume
        from its reserves, and informs the agent about the amount of sugar received"""
        self.reserve = self.reserve + sugar - self.consume
        self.agent.feed(sugar)