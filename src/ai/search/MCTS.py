import math
import random
from typing import List, Tuple
from src.environment.agent_handler import Agent_Handler
from src.environment.map import Map



class MCTSNode:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []
        self.visits = 0
        self.value = 0
        
    def expand(self): 
        #? Actua el agente principal en cuestion? 
        #* Si, se expande de acuerdo a las decisiones del agente principald
        #* por cada una de las posibles acciones en ese escenario todos los agentes toman una decisión
        #* Estás dependen de si se conoce el tipo de los agentes enemigos, del agente que se desconosca su tipo 
        #* (Enemigo o no) actuara random 

        # Será que se expande según la función heuristica propia del tipo de agente?
        possible_actions = self.state.get_possible_actions() # Dame las posibles acciones de mi agente en este turno  
        for action in possible_actions: 
            new_state = self.state.ChildState(action) #Crea un estado resultante de hacer la acción
            new_node = MCTSNode(new_state) #Crea un nodo para ese escenario 
            new_node.parent = self 
            self.children.append(new_node)

    def select_child(self):
        # Select a child node using the UCB1 formula
        exploration_constant = 1.4
        best_child = None
        best_score = -math.inf
        for child in self.children:
            score = child.value / (child.visits + 1) + exploration_constant * math.sqrt(math.log(self.visits + 1) / (child.visits + 1))
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

    def backpropagate(self, value):
        # Update the value and visit count of the node and its ancestors
        self.visits += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(value)




class MCTS:
    def __init__(self, iterations=1000, depth = 0):
        self.iterations = iterations
        self.depth = depth

    def select_action(self, agent: Agent_Handler):
        state = State(agent) #!Tacto se crea un estado inicial
        root = MCTSNode(state)

        for _ in range(self.iterations):
            node = root
            # Select
            while not node.state.is_terminal() and len(node.children) > 0: # No es terminal y No es hoja
                node = node.select_child()
            # Expand
            if not node.state.is_terminal() and len(node.children) == 0: # No es un estado terminal y es hoja
                node.expand()
                node = random.choice(node.children) # Random en este punto?
                # TODO Este random funciona con las hojas recién descubiertas
            # Simulate
            simulated_value = self.simulate(node.state) # 
            # Backpropagate
            node.backpropagate(simulated_value)
        # Select the best action based on the most visited child
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state.last_action

    def simulate(self, state):
        # Simula un juego completamente random a partir del estado actual
        if not state.is_terminal():
            action = random.choice(state.get_possible_actions())
            aux_state = state.ChildState(action)
        while not state.is_terminal():
            action = random.choice(state.get_possible_actions())
            aux_state.ChildState(action) # El estado original no es una hoja
        return aux_state.get_result()
    
    


class State:
    def __init__(self, agent: Agent_Handler) -> None:
        self.map = {}
        self.agents = 0 #TODO Esto lo dará el conocimiento que agente principal sobre los otros personajes 
        pass # Crear un mapa de acuerdo a la imagen 

    def CreateMap(self): 
        #? Este método debe crear un map según lo que vio el agente
        #? El agente debe ...
        #! Este método emplear probilidades para generar de manera random recursos y agentes en la zona fuera del campo de visión real del agente primario
        width, height = 10 # TODO Estos números los conoce el agente según las dimensiones originales del mapa, !!!Cambiar
        resources = {}
        for i in range(width):
            for j in range(height):
                # if El agente vio o ve recursos en esa posición agrega ese recurso en esa cantidad
                    #continue
                if random.choices([True, False]):
                    resources[(i, j)] = random.randint(
                        1, 100
                    )  
        self.map = Map(width, height, resources)

        
        # posición de los agentes que recuerda el agente primario

        # sacar un random a partir de los agentes que desconoce el agente
        #! Está la posibilidad que se identifique un mismo agente como varios en distintos momentos, Creandose un escenario erroneo 
        #! Qué se haría en este caso? OJO!!! 
        
        #! Colocar los agentes en el mapa
        
        pass 

    #* Creo que este esta listo 
    def get_possible_actions(self): #? Debe devolver una lista de 3-uplas (movimiento, ataque, alianza) 
        #TODO Saca las posibles acciones del agente primario
        association_proposals = self.get_association_proposals()
        attacks = self.agent.get_attacks() 
        moves = self.get_moves()

        actions = []
        #Crea todas las posibles 3-uplas (Las posibles acciones del agente principal)
        for move in moves:
            for attack in attacks:
                for association in association_proposals:
                    actions.append(tuple[move, attack, association])
                    
        return actions
    
    def PlayRound(self, action: tuple): #TODO Recibe una 3-upla (movimiento, ataque, alianza) del agente principal
        #TODO Se juega una ronda completa con la decisión del agente principal y después el resto de agente
        #for character in agents 
            #association_proposals = character.get_association_proposals() #TODO No sé como modelar estás la alianzas
            #attacks = character.get_attacks()
            #moves = character.get_moves()
            #TODO aplicar estas acciones en el estado
        return 
    def ChildState():
        
        pass
    
    def is_Terminal():
        #TODO Es Terminal si vence o se muere
        #* return self.agent.IsDead() or enemigos == 0
        pass
    def ValueState(): 
        #!Como uno evalua el estado?
        #*Tengo claro que Menos infinito si en este escenario el agente principal está muerto
        #TODO Pensar en criterios para la evaluación de un estado
        pass 
