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
            distance = max(abs(self.position[0] - other_agent_position[0]) + abs(self.position[1] - other_agent_position[1]), 1)
            agresivity = self.computated_agresivities[agent_id]
            risk += (agresivity*other_agent_sugar)/(distance*max(self.reserves, 1))
        return risk
    
    def get_association_proposals(self) -> List[Association_Proposal]:
        return []
    
    def get_attacks(self) -> List[Attack]:
        return []
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        return False