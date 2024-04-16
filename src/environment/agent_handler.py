from typing import Tuple, Dict, List
from Interfaces.IAgent import IAgent
from Interfaces.IRange import IRange
from Interfaces.IMovement import IMovement
from Interfaces.IVision import IVision
from Interfaces.IAttack_Range import IAttackRange
from map import Map
from sim_object import Sim_Object, Sim_Object_Type
from actions import Action_Info, Action
from association import Association

class Agent_Handler(Sim_Object):
    def __init__(self, id : int, reserve : int, consume : int, map : Map, agent : IAgent, movement : IMovement, vision : IVision, attack_range : IAttackRange):
        super().__init__(id, Sim_Object_Type.AGENT)
        self.reserve = reserve
        self.consume = consume
        self.map = map
        self.agent = agent
        self.movement = movement
        self.vision = vision
        self.attack_range = attack_range
        self.associations : Dict[int, Association] = {}
        self.free_portion = 1
    
    @property
    def IsDead(self):
        return (self.reserve < 0)
    
    @property
    def IsAssociated(self):
        return len(self.associations) > 0
    
    def move(self) -> Tuple[int, int]:
        "Gets the position the agent wants to move to"
        possible_moves = self.movement.moves(self.map, self.id)
        return self.agent.move(possible_moves)
    
    def inform_move(self, position : Tuple[int, int]) -> None:
        "Informs the agent he has moved to the given position"
        return self.agent.inform_move(position)
    
    def get_actions(self) -> List[Action]:
        possible_actions = self.attack_range.possible_victims(self.map, self.id)
        actions_taken : List[Action] = self.agent.get_actions(possible_actions)
        for action in actions_taken:
            action.actor_id = self.id
        return actions_taken
    
    def inform_of_attack_made(self, victim_id : int, strength : int) -> None:
        "Informs the agent that an attack that he has requested, has been executed"
        self.reserve -= strength
        return self.agent.inform_of_attack_made(victim_id, strength)
    
    def inform_of_attack_received(self, attacker_id : int, strength : int) -> None:
        "Informs the agent of an attack he has received"
        self.reserve -= strength
        return_value = self.agent.inform_of_received_attack(attacker_id, strength)
        return return_value
    
    def take_attack_reward(self, victim_id : int, reward : int):
        """Informs the agent of the reward obtained by killing an agent, and actualizes
        its reserves"""
        self.reserve += reward
        return self.agent.take_attack_reward(victim_id, reward)
    
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
        vision = self.vision.see_actions(self.map, self.id)
        self.agent.see_actions(vision)
    
    def feed(self, sugar : int) -> None:
        """Increaes the agent reserves with the amount of sugar given, and informs the agent"""
        self.reserve = self.reserve + sugar
        self.agent.feed(sugar)
    
    def burn(self) -> None:
        """Dimishes the agent reserves by his diary consume."""
        self.reserve = self.reserve - self.consume
        self.agent.burn()