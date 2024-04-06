import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/enviroment')
sys.path.insert(0, current_dir + '/src/ai')
sys.path.insert(0, current_dir + '/src/interfaces')
from Interfaces.IAgent import IAgent
from environment.actions import Action, Alliance_Solicitude
from environment.objects import Object_Info
from typing import List, Tuple
class Agent_Handler():
    """El manejador de Agente de la simulacion
    """
    def __init__(self, id, health : int, ammo : int, range_of_vision : int, agent : IAgent):
        self.id = id
        self.health = health
        self.ammo = ammo
        self.range_of_vision = range_of_vision
        self.agent = agent
    
    def move(self) -> Tuple[int, int]:
        return self.agent.move()
    
    def actions(self) -> List[Action]:
        """Obtener una lista de las acciones que realizara el agente durante el turno"""
        return self.agent.actions()
    
    def actualize_personal_info(self):
        self.agent.actualize_personal_info(self.x, self.y, self.health, self.ammo)
    
    def falled_in_trap(self):
        self.agent.falled_in_trap()
        self.actualize_personal_info()

    def received_attack(self):
        self.agent.received_attack()
        self.actualize_personal_info()
    
    def view(self, sight : List[Tuple[int, int, Object_Info]]):
        self.agent.view(sight)