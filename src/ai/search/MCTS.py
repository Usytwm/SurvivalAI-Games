import math
import random
from src.environment.agent_handler import Agent_Handler

class MCTSNode:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []
        self.visits = 0
        self.value = 0
        
    def expand(self): #? Actua el agente en cuestion? Respuesta Si, se expande de acuerdo a las decisiones
                      #? primario, por cada una de las posibles acciones en ese escenario todos los agentes toman una decisión
                      #? Estás dependen de si se conoce el tipo de los agentes enemigos, del agente que se desconosca su tipo 
                      #? (Enemigo o no) actuara random 
        # Expand the node by adding child nodes for all possible actions
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
        # Simulate a random game from the current state and return the result
        while not state.is_terminal():
            action = random.choice(state.get_possible_actions())
            state = state.perform_action(action)
        return state.get_result()
    
#? Este método debe crear un map según lo que vio el agente
#? El agente debe ...
    def CreateState(agent: Agent_Handler):
        pass   

class State:
    def __init__(self, agent: Agent_Handler) -> None:
        pass # Crear un mapa de acuerdo a la imagen 
    def ChildState():
        #!Clona el escenario
        pass
    def isTerminal():
        #!Es Terminal si vence o se muere
        pass
    def ValueState(): 
        #!Como uno evalua el estado?
        #? Menos infinito si en este escenario está muerto
        pass 
