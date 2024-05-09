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
        self.minimun_free_portion = 0.1
        self.appeal_recquired_to_associate = 0.5
        self.attacks_planned = []
        self.association_proposals_planned = []
        self.computated_agresivities : Dict[int, int] = {}

    def decide_actions_for_next_turn(self):
        self.actualize_agresivities()
        self.attacks_planned, agents_to_extorsion = self.decide_attacks_for_next_turn()
        self.association_proposals_planned = self.decide_association_proposals_for_next_turn(agents_to_extorsion)

    def move(self, possible_moves: List[Tuple[int]]) -> Tuple[int]:
        destinations = [((self.position[0] + move[0], self.position[1] + move[1]), move) for move in possible_moves]
        destinations = [(self.evaluate_position(position), move) for position, move in destinations]
        destinations.sort(key= lambda tpl : tpl[0], reverse= True)
        return destinations[0][1]
    
    def get_association_proposals(self) -> List[Association_Proposal]:
        return self.association_proposals_planned
    
    def get_attacks(self) -> List[Attack]:
        return self.attacks_planned
    
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
    
    def decide_association_proposals_for_next_turn(self, agents_to_extorsion : List[int]) -> List[Association_Proposal]:
        """A los agentes extorsionables los extorsionamos. A los agentes que son capaces de
        destruirnos y tienen cierta agresividad les ofrecemos alianzas ventajosas para ellos 
        (pero no tanto Xd). A los restantes agentes decidimos ofrecerles alianzas si nos parece
        lo suficientemente atractiva una asociacion con ellos. Cuan atractiva nos parece una
        asociacion estara dado por una formulita"""
        association_proposals = []
        for victim_id in agents_to_extorsion:
            commitments = {victim_id : (0.25, 0), self.id : (0, 1)}
            association_proposals.append(Association_Proposal(victim_id, [self.id, victim_id], commitments))
        direct_threats : List[Tuple[int, int, int]] = [] #[(other_id, other_resources, other_distance)]
        par_agents : List[Tuple[int, int, int]] = [] #[(other_id, other_resources, other_distance)]
        for other_id in self.memory_for_agents_sights.agents_seen:
            if other_id in self.memory_for_attacks.deaths or other_id in agents_to_extorsion:
                continue
            other_position, _, other_resources = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
            distance = abs(other_position[0] - self.position[0]) + abs(other_position[1] - self.position[0])
            if (distance <= 3) and (other_resources > self.reserves) and self.computated_agresivities[other_id] >= 0.25:
                direct_threats.append((other_id, other_resources, distance))
            else:
                par_agents.append((other_id, other_resources, distance))
        #Ordenamos las amenazas directas por agresividad y distancia en ese orden
        left_free_portion = self.free_portion
        direct_threats.sort(key= lambda tpl : (self.computated_agresivities[tpl[0]], tpl[2]), reverse= True)
        fractions_to_sacrifice = self.get_fractions_to_sacrifice(direct_threats)
        idx = 0
        for other_id, other_resources, distance in direct_threats:
            left_free_portion -= fractions_to_sacrifice[idx]
            commitments = {self.id : [fractions_to_sacrifice[idx], 0], other_id : [0, 1]}
            association_proposals.append(Association_Proposal(self.id, [self.id, other_id], commitments))
            idx += 1
        par_agents = [(id, self.kill_apeal_formula(distance, self.computated_agresivities[id])) for id, _, distance in par_agents]
        par_agents.sort(key= lambda tpl : tpl[1], reverse= True)
        for other_id, appeal in par_agents:
            if appeal < self.appeal_recquired_to_associate:
                break
            commitments = {self.id : (0, 0), other_id : (0, 0)}
            association_proposals.append(Association_Proposal(self.id, [self.id, other_id], commitments))
        return association_proposals
    
    def decide_attacks_for_next_turn(self) -> Tuple[List[Attack], List[int]]:
        """Este metodo devuelve los ataques a realizar en el proximo turno, asi como una lista
        de aquellos agentes que pueden ser extorsionados, ya q no fue posible atacarlos pero se
        encuentran en una situacion de debilidad respecto al agente.\n
        Por ahora solo se realizan ataques a agentes que sabemos exclusivamente que podemos
        destruir, y solo realiza ataques mientras cumpla que la proporcion de las reservas que
        quedan tras el ataque con respecto al riesgo de la posicion actual es mayor que el umbral
        de seguridad. Aquellos agentes que pudieran ser destruidos, pero que no fueron atacados
        para mantener la invariante del umbral de seguridad, son anhadidos a la lista de agentes
        extorsionables. Los agentes son procesados en el orden de cuan atractivo seria matarlos,
        calculo que esta dado por una formulita"""

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
        agents_to_extorsion = []
        risk = self.get_risk_of_position(self.position)
        left_reserves = self.reserves
        for other_id, strength_needed, target_apeal in killable_agents:
            if (left_reserves - strength_needed)/risk > self.security_umbral:
                attacks_to_kill.append(Attack(self.id, other_id, strength_needed))
                left_reserves -= strength_needed
            else:
                agents_to_extorsion.append(other_id)
        attacks.extend(attacks_to_kill)
        return attacks, agents_to_extorsion
    
    def evaluate_attack_to_kill(self, other_id) -> Tuple[bool, int, float]:
        """Dado el id de otro agente, este metodo determina si es posible matarlo con un ataque
        en este turno, la fuerza que debe tener tal ataque y el atractivo que tiene matar a tal
        agente."""
        other_position, _, other_resources = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
        other_expected_resources = other_resources + self.geographic_memory.get_max_sugar_around_position(other_position[0], other_position[1])
        if other_expected_resources < self.reserves:
            return (True, other_expected_resources, self.kill_apeal(other_id, other_position))
        return (False, None, self.kill_apeal(other_id, other_position))
    
    def get_fractions_to_sacrifice(self, direct_threats : List[Tuple[int, int, int]]):
        """Por ahora es sencilla"""
        fractions_to_sacrifice = []
        if (len(direct_threats) == 1):
            return [min(0.33, self.free_portion - self.minimun_free_portion)]
        if (len(direct_threats) < 3) and (self.free_portion - 0.3 > self.minimun_free_portion):
            return [0.2, 0.1]
        for i in range(len(direct_threats)):
            fractions_to_sacrifice.append(min(0.1, self.free_portion - self.minimun_free_portion))
        return fractions_to_sacrifice
    
    def kill_apeal(self, other_id : int, other_position : Tuple[int, int]) -> float:
        """Dado un agente, devuelve cuan atractiva es la idea de matarlo. Para esto se basa de
        una formula, donde el parametro Beta, distribuye el peso de la importancia de matar a 
        otro agent entre su cercania y su agresividad"""
        distance = max(abs(self.position[0] - other_position[0]) + abs(self.position[1] - other_position[1]), 1)
        agresivity = self.computated_agresivities.get(other_id, 0)
        return self.kill_apeal_formula(distance, agresivity)
    
    def kill_apeal_formula(self, distance : int, agresivity : int):
        return self.beta*(1/max(distance, 1)) + (1 - self.beta)*agresivity
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        risk = self.get_risk_of_position(self.position)
        some_easy_victim_trying_to_scape = False
        kill_apeals = []
        #-Si alguno de los miembros puede matarme y tengo los recursos para pagarla, acepto
        for other_id in proposal.members:
            if not other_id in self.memory_for_agents_sights.agents_seen:
                continue
            other_position, _, other_resources = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
            distance = abs(other_position[0] - self.position[0]) + abs(other_position[1] - self.position[1])
            if (other_resources > self.reserves) and (distance <= 3) and (self.free_portion - proposal.commitments[self.id][0] > self.minimun_free_portion):
                return True
            is_killable, strength_needed, target_apeal = self.evaluate_attack_to_kill(other_id)
            if is_killable and (self.reserves - strength_needed)/risk > self.security_umbral:
                some_easy_victim_trying_to_scape = True
            kill_apeals.append(target_apeal)
        #-Si es alguien a quien puedo matar en este turno, digo no
        if some_easy_victim_trying_to_scape:
            return False
        #-Si no me toma recursos queda por ver si la kill_apeal entra en caja
        for kill_apeal in kill_apeals:
            if kill_apeal < self.appeal_recquired_to_associate:
                return False
        return True
    
    def see_resources(self, info: List[Tuple[Tuple[int] | int]]) -> None:
        super().see_resources(info)
        self.decide_actions_for_next_turn()