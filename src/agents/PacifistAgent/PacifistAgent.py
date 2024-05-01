import sqlite3
from typing import Dict, List, Tuple

from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info, Association_Proposal
from environment.sim_object import Object_Info
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange

class PacifistAgent(Agent_with_Memories):
    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        super().__init__(id, consume, reserves, conn, movement, attack_range)
        self.color = (0, 0, 255)  # blue

    def move(self):
        """A cada posible movimiento se le asocia una tupla que contiene como primer elemento
        el riesgo asociado a una posicion y como segundo elemento la ganancia asociada a una
        posicion con signo negativo. Luego se ordenan las posiciones en orden ascendente de sus
        tuplas, y se selecciona la primera como proximo movimiento"""
        posible_movements = self.movement.pure_moves()
        peligrosities : Dict[int, Tuple[int, Tuple[int, int]]] = self.__calculate_peligrosities__()
        best_move = min(posible_movements, key= lambda x : self.__evaluate_risk_of_movement__(peligrosities, x))
        return best_move
    
    
    def __calculate_peligrosities__(self) -> Dict[int, Tuple[float, Tuple[int, int]]]:
        """Devuelve un diccionario donde a cada agente le hace corresponder una tupla con su
        peligrosidad y su ultima posicion conocida.\n
        La peligrosidad la calcula multiplicando los recursos que llevaba ese agente consigo la
        ultima vez que fue visto, por la cantidad de ataques que el agente le ha visto realizar
        entre la cantidad de veces que ha sido visto"""
        answer = {}
        for id in self.memory_for_agents_sights.agents_seen:
            last_position, iteration, sugar = self.memory_for_agents_sights.get_last_info_from_agent(id)
            peligrosity = (sugar*self.memory_for_attacks.num_of_attacks_by_agent.get(id, 0))/self.memory_for_agents_sights.agents_seen[id]
            answer[id] = (peligrosity, last_position)
        return answer

    def __evaluate_risk_of_movement__(self, peligrosities : Dict[int, Tuple[float, Tuple[int, int]]], movement : Tuple[int, int]) -> Tuple[float, int]:
        """Dado un diccionario que a cada agente conocido le hace corresponder su peligrosidad
        y su posicion; y una casilla, devuelve una tupla cuyo primer elemento es cuan riesgoso
        parece ser moverse a esa casilla y su segundo elemento es la ganancia de azucar de esa 
        casilla multiplicada por -1. De esta manera la menor de todas esas tuplas correspondera 
        a la casilla mas segura"""
        #Cada agente violento incrementa el riesgo de una posicion en el inverso de su distancia
        #a esa posicion, multiplicado por su peligrosidad
        new_position = (self.position[0] + movement[0], self.position[1] + movement[1])
        if movement == (0, 0):
            sugar = -1
        else:
            try:
                sugar = self.geographic_memory.get_last_info_of_sugar_in_position(new_position[0], new_position[1])[1]
            except:
                sugar = 0 #si no sabemos cuanta azucar hay asumimos 0, eso no esta bien pero bueno
        risk = 0
        for id in self.memory_for_agents_sights.agents_seen:
            peligrosity, position = peligrosities[id]
            distance = abs(new_position[0] - position[0]) + abs(new_position[1] - position[1])
            risk = risk + peligrosity*(1/max(distance, 1))
        return (risk, -sugar)

    def get_attacks(self) -> List[Action]:
        return []

    def get_association_proposals(self) -> List[Association_Proposal]:
        """Por ahora tratan de asociarse a todos los agentes que ven"""
        answer = []
        for agent_id in self.memory_for_agents_sights.agents_seen:
            if not agent_id in self.allys:
                commitments = {self.id : (0, 0), agent_id : (0, 0)}
                answer.append(Association_Proposal(self.id, [self.id, agent_id], commitments))
        return answer

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        "Devuelve si el agente acepta ser parte de la asociacion o no"
        return True