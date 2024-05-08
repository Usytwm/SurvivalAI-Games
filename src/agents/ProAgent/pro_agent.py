import sqlite3
import random
from typing import List, Tuple, Dict
from agents.Agent_with_Memories import Agent_with_Memories
from environment.actions import Association_Proposal, Attack
from Interfaces.IAgent import IAgent
class ProAgent(Agent_with_Memories):
    def __init__(self, id: int, consume: int, reserves, conn: sqlite3.Connection):
        super().__init__(id, consume, reserves, conn)
        self.color = (160, 32, 240)#purple
        self.alfa = 0.5
        self.beta = 0.5
        self.security_umbral = 1
        self.computated_agresivities : Dict[int, int] = {}

    def move(self, possible_moves: List[Tuple[int]]) -> Tuple[int]:
        self.actualize_agresivities()
        destinations = [((self.position[0] + move[0], self.position[1] + move[1]), move) for move in possible_moves]
        destinations = [(self.evaluate_position(position), move) for position, move in destinations]
        destinations.sort(key= lambda tpl : tpl[0], reverse= True)
        return destinations[0][1]
    
    def actualize_agresivities(self) -> None:
        for agent_id in self.memory_for_agents_sights.agents_seen:
            self.computated_agresivities[agent_id] = self.memory_for_attacks.attacks_per_agent.get(agent_id, 0)/self.memory_for_agents_sights.agents_seen[agent_id]
    
    def evaluate_position(self, position : Tuple[int, int]) -> float:
        sugar = self.geographic_memory.get_last_info_of_sugar_in_position(position[0], position[1])[1]
        risk = self.get_risk_of_position(position)
        return self.alfa*sugar - (1 - self.alfa)*risk
    
    def get_risk_of_position(self, position : Tuple[int, int]) -> float:
        risk = 0
        for agent_id in self.memory_for_agents_sights.agents_seen:
            if agent_id in self.memory_for_attacks.deaths:
                continue
            other_agent_position, _, other_agent_sugar = self.memory_for_agents_sights.get_last_info_from_agent(agent_id)
            distance = max(abs(position[0] - other_agent_position[0]) + abs(position[1] - other_agent_position[1]), 1)
            agresivity = self.computated_agresivities.get(agent_id, 0)
            risk += (agresivity*other_agent_sugar)/(distance)
        return max(risk, 1)
    
    def get_association_proposals(self) -> List[Association_Proposal]:
        return []
    
    def get_attacks(self) -> List[Attack]:
        """Mientras la proporcion entre la cantidad de azucar que tengo y el riesgo en la casilla
        en que me encuentro sea mayor que el umbral de seguridad, ataco a aquellos agentes que 
        puedo destruir. Para seleccionar cuales de todos los que puedo atacar ataco, uso una
        formula que combina la distancia a la que me encuentro del agente y su nivel de violencia"""
        attacks = []
        killable_agents : List[Tuple[int, int, float]] = [] #id, fuerza_requerida, formulita
        for other_id in self.memory_for_agents_sights.agents_seen:
            if other_id in self.memory_for_attacks.deaths:
                continue
            is_vulnerable, strength_needed, target_apeal = self.evaluate_attack_to_kill(other_id)
            if is_vulnerable:
                killable_agents.append((other_id, strength_needed, target_apeal))
        killable_agents.sort(key= lambda tpl : tpl[2], reverse= True)

        attacks_to_kill = []
        risk = self.get_risk_of_position(self.position)
        left_reserves = self.reserves
        for other_id, strength_needed, target_apeal in killable_agents:
            if (left_reserves - strength_needed)/risk > self.security_umbral:
                attacks_to_kill.append(Attack(self.id, other_id, strength_needed))
                left_reserves -= strength_needed
        attacks.extend(attacks_to_kill)
        return attacks
    
    def evaluate_attack_to_kill(self, other_id) -> Tuple[bool, int, float]:
        """Dado el id de otro agente, este metodo determina si es posible matarlo con un ataque
        en este turno, la fuerza que debe tener tal ataque y el atractivo que tiene matar a tal
        agente."""
        other_position, _, other_resources = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
        other_expected_resources = other_resources + self.geographic_memory.get_max_sugar_around_position(other_position[0], other_position[1])
        if other_expected_resources < self.reserves:
            return (True, other_expected_resources, self.kill_apeal(other_id, other_position))
        return (False, None, None)
    
    def kill_apeal(self, other_id : int, other_position : Tuple[int, int]) -> float:
        """Dado un agente, devuelve cuan atractiva es la idea de matarlo. Para esto se basa de
        una formula, donde el parametro Beta, distribuye el peso de la importancia de matar a 
        otro agent entre su cercania y su agresividad"""
        distance = max(abs(self.position[0] - other_position[0]) + abs(self.position[1] - other_position[1]), 1)
        agresivity = self.computated_agresivities.get(other_id, 0)
        return self.beta*(1/distance) + (1 - self.beta)*agresivity
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        return False