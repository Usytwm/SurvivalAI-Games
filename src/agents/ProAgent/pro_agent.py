import sqlite3
import random
from typing import List, Tuple
from agents.Agent_with_Memories import Agent_with_Memories
from environment.actions import Association_Proposal, Attack
from Interfaces.IAgent import IAgent
class ProAgent(Agent_with_Memories):
    def __init__(self, id: int, consume: int, reserves, conn: sqlite3.Connection):
        super().__init__(id, consume, reserves, conn)
        self.color = (160, 32, 240)#purple
        self.alfa = 0.5

    def move(self, possible_moves: List[Tuple[int]]) -> Tuple[int]:
        return (0, 0)
    
    def get_association_proposals(self) -> List[Association_Proposal]:
        return []
    
    def get_attacks(self) -> List[Attack]:
        return []
    
    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        return False