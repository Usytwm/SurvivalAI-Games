import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/enviroment')
sys.path.insert(0, current_dir + '/src/ai')
sys.path.insert(0, current_dir + '/src/interfaces')
from typing import List, Tuple, Dict
from environment.objects import Sim_Object, Object_Type, Presence, Agent_Image, Empty
from environment.agent_handler import Agent_Handler
from environment.map_controller import Map
from environment.actions import Action, ActionType
from Interfaces.IAgent import IAgent
from random import randint

class GameController:
    def __init__(self, width, height, objects : List[Tuple[int, int, Sim_Object]], agents : Dict[str, IAgent]):
        self.map = Map(width, height)
        self.objects : Dict[str, Sim_Object] = {}
        self.agents : Dict[str, Agent_Handler] = {}
        for x, y, obj in objects:
            self.objects[obj.id] = obj
            if obj.id in agents:
                handler = Agent_Handler(obj.id, randint(1, 3), 100, randint(1, 5), agents[obj.id])
                self.agents[obj.id] = handler
            self.map.add_object(x, y, obj.id)
    
    def step(self):
        alliance_solicitudes = {} #Este sera un diccionario donde a cada agente le hacemos corresponder una lista con las solicitudes de alianzas que realiza en el turno
        actions = {} #Este sera un diccionario donde a cada agente le hacemos corresponder una lista de sus acciones
        moves = {} #Este sera un diccionario donde a cada agente le hacemos corresponder su movimiento
        dict_of_move_destinations = {} #Creamos un conjunto con todos los lugares a donde desean moverse los agentes para evitar movimientos duplicados
        
        def pick_agents_activities():
            for agent_id in self.agents:
                agent = self.agents[agent_id]
                actions[agent_id] = agent.actions()
                moves[agent_id] = agent.move()

        def manage_alliances():
            pass

        def manage_actions():
            for agent_id in self.agents:
                for action in actions[agent_id]:
                    action = Action(action.type, agent_id, action.direction)
                    self.execute_action(action)
                    #self.agents[agent_id].actualize_personal_info()
        
        def erase_dead_agents():
            dead_agents = set()
            for agent_id in self.agents:
                agent = self.agents[agent_id]
                if agent.health <= 0:
                    x, y = self.map.object_positions[agent_id]
                    self.map.remove_object(x, y, is_agent= True)
                    dead_agents.add(agent_id)
            for agent_id in dead_agents:
                self.objects.pop(agent_id)
                self.agents.pop(agent_id)

        def collect_destinations():
            """Llena dict_of_move_destinations. Tal diccionario guarda para cada casilla de
            destino todos los agentes que trataran de acceder a ella
            """
            for agent_id in self.agents:
                destination = self.map.object_positions[agent_id]
                destination = (destination[0] + moves[agent_id][0], destination[1] + moves[agent_id][1])
                if destination in dict_of_move_destinations:
                    dict_of_move_destinations[destination].append(agent_id)
                else:
                    dict_of_move_destinations[destination] = [agent_id]

        def manage_moves():
            collect_destinations()
            for destination in dict_of_move_destinations:
                if len(dict_of_move_destinations[destination]) == 1:
                    agent_id = dict_of_move_destinations[destination][0]
                    origin = self.map.object_positions[agent_id]
                    self.map.move(origin[0], origin[1], destination[0], destination[1])
        
        def update_agents_vision():
            pass
        """
            for agent_id in self.agents:
                pos_x, pos_y = self.map.object_positions[agent_id]
                sight = self.map.peek_from(pos_x, pos_y, self.get_range_of_vision(agent_id))
                sights_for_agent = []
                for x, y, id, nitidez in sight:
                    sights_for_agent.append((x, y, self.get_object_image(x, y, id, nitidez)))
                self.agents[agent_id].view(sights_for_agent)
"""
                
        pick_agents_activities()
        manage_alliances()
        manage_actions()
        erase_dead_agents()
        manage_moves()
        update_agents_vision()
        self.display()

    def execute_action(self, action : Action):
        match action.type:
            case ActionType.ATTACK:
                self.manage_attack(action.agent, action.direction, action.intensity)
    
    def manage_attack(self, agent_id : str, direction : Tuple[int, int], intensity : int):
        print("Agente " + str(agent_id) + " ataca en direccion " + str(direction))
        self.agents[agent_id].ammo -= intensity
        max_length = self.get_max_length_of_attack(agent_id, intensity)
        object_hit_id, distance = self.map.shot(agent_id, direction, max_length)
        if object_hit_id == None:
            return
        if object_hit_id in self.agents:
            agent_hit = self.agents[object_hit_id]
            print("Agente " + str(object_hit_id) + " fue golpeado, le quedan " + str(agent_hit.health) + " vidas")
            damage = self.get_damage_of_attack(object_hit_id, distance)
            agent_hit.health -= damage

    #Metodos ajustables
    def get_max_length_of_attack(self, agent_id : str, intensity : int):
        return 5
    
    def get_damage_of_attack(self, agent_hit_id : str, distance : int):
        return 1
    
    """
    def get_range_of_vision(self, agent_id):
        #Aqui podremos hacer cosas mas complejas como q la vision disminuya al
        #disminuir la salud y demas
        return self.agents[agent_id].range_of_vision
    
    def get_object_image(self, x : int, y : int, id : str, nitidez : int):
        #La nitidez va de 1 a 0, mientras menor la nitidez menos detalles sabemos.
        #Por ahora siempre sabemos todos los detalles, pero despues debemos ajustarlo
        if id is None:
            return Empty()
        if nitidez <= 0.25:
            return Presence()
        if id in self.agents:
            image = Agent_Image() if id in self.agents else None #No hemos implementado aun los demas casos de cosas visibles
            if nitidez >= 0.3:
                image.id = id
            if nitidez >= 0.5:
                image.health = self.agents[id].health
                image.ammo = self.agents[id].ammo
        return image
    """
    def display(self):
        self.map.display()