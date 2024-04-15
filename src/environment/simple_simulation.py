"""En esta simulacion simple consideramos lo siguiente, por motivos de simplicidad:
1- Si dos agentes deciden moverse a la misma casilla, ambos se quedan donde estan
2- Los ataques funcionan de la sgte manera:
   - Para realizar un ataque de fuerza k, el atacante debe gastar k azucar
   - Si un agente resulta muerto producto de un ataque, toda su riqueza se distribuye
   entre aquellos que lo atacaron de manera proporcional a la fuerza de sus ataques
   - Una vez que un ataque llega al metodo __execute_attack__, se raliza, no importa si
   durante la ejecucion de tal metodo el agente resulta muerto antes de que el ataque que
   lanzo sea analizado
"""
from typing import Dict, Tuple, List, Set
from Interfaces.ISimulation import ISimulation
from environment.actions import Action
from environment.graph_of_attacks import Graph_of_Attacks, Component_of_Attacks_Graph
class SimpleSimulation(ISimulation):
    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        moves = {}
        destinations : Dict[Tuple[int, int], List[int]] = {}
        
        for id, agent in self.agents.items():
            mov_X, mov_Y = agent.move()
            current_X, current_Y = self.map.peek_id(id)
            destiny = (mov_X + current_X, mov_Y + current_Y)
            if not destiny in destinations:
                destinations[destiny] = []
            destinations[destiny].append(id)
        
        for destiny, travellers in destinations.items():
            if len(travellers) > 1:
                for id in travellers:
                    moves[id] = self.map.peek_id(id) #o sea, no se mueve
            else:
                moves[travellers[0]] = destiny
        
        return moves
    
    def __execute_actions__(self, actions: Dict[int, List[Action]]):
        initial_wealth = {id : agent.reserve for id, agent in self.agents.items()}
        graph_of_attacks = Graph_of_Attacks(actions)
        if not graph_of_attacks.empty:
            for attack in graph_of_attacks.connected_components():
                self.__execute_attack__(attack, initial_wealth)
        #Formalize asociations
        pass

    
    #Usamos esta modelacion de los ataques como grafos por su expresividad, porque 
    #perfectamente nos podra servir para implementar logicas de combate mas complejas, como
    #que si un agente recibe multiples ataques recibe mayor danho al no poder protegerse.
    #Pero para la implementacion simple actual, daria lo mismo usar esta simulacion de grafos
    #como sencillamente una lista con todos los ataques que suceden en el turno
    def __execute_attack__(self, graph : Component_of_Attacks_Graph, initial_wealth : Dict[int, int]):
        """Este metodo recibe una de las peleas, descrita como un componente conexo del grafo
        y ademas recibe las riquezas iniciales de los agentes. Ejecuta cada uno de los ataques,
        cobrando a cada agente su costo, infligiendo danhos y repartiendo las riquezas que
        inicialmente tenia un agente entre los agentes que lo atacaron de manera proporcional
        a la fuerza con que lo hicieron 
        """
        #attackers almacena para cada agente quien lo ataco y la fuerzo con que lo ataco.
        #Esto es util para luego repartir de manera proprocional la riqueza inicial de la victima
        #entre los atacantes
        attackers : Dict[int, Dict[int, int]] = {}
        deads = set()

        for actor_id, attacks_dict in graph.edges.items():
            for victim_id, attack_strength in attacks_dict.items():
                self.agents[actor_id].inform_of_attack_made(victim_id, attack_strength) #el costo de realizar el ataque
                self.agents[victim_id].inform_of_attack_received(actor_id, attack_strength) #el danho que realiza
                if self.agents[victim_id].IsDead:
                    deads.add(victim_id)
                if not victim_id in attackers:
                    attackers[victim_id] = {}
                attackers[victim_id][actor_id] = attack_strength
        
        for dead_id in deads:
            sum_of_strengths = sum(attackers[dead_id].values())
            for attacker_id, attack_strength in attackers[dead_id].items():
                reward = int((attack_strength*initial_wealth[dead_id])/sum_of_strengths)
                self.agents[attacker_id].take_attack_reward(dead_id, reward)

    def display(self):
        print("____________________")
        for row in range(0, self.map.height):
            line = ""
            for column in range(0, self.map.width):
                content = self.map.peek_from_position((row, column))
                content = content if content else " "
                line = line + str(content) + " "
            line = line + '|'
            print(line)
        print("____________________")