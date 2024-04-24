from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict


class Knowledge(Enum):
    POSITION = "position"
    RESERVE = "reserve"
    HEALTH = "health"
    ATTACKS = "attacks"
    ASSOCIATION_PROPOSALS = "association_proposals"
    ATTACK_MADE = "attack_made"
    RECEIVED_ATTACK = "received_attack"
    ATTACK_REWARD = "attack_reward"
    SEE_OBJECTS = "see_objects"
    SEE_RESOURCES = "see_resources"
    SEE_ACTIONS = "see_actions"
    FEED = "feed"
    BURN = "burn"
    POSIBLES_MOVEMENTS = "posibles_movements"
    ALLIES = "allies"
    ENEMIES = "enemies"
    AGEENTS = "agents"


class BaseKnowledge(ABC):

    @abstractmethod
    def learn(self, data: Dict[Knowledge, Any]):
        """
        Aprende del entorno o de los datos proporcionados.
        """
        pass

    @abstractmethod
    def learn_especific(self, key: Knowledge, data: Any):
        """
        Aprende del entorno un solo conocimiento.
        """
        pass

    @abstractmethod
    def make_decision(self):
        """
        Toma una decisión basada en la base de conocimientos actual.
        """
        pass

    def get_knowledge(self, key: Knowledge):
        """
        Retorna un conocimiento específico.
        """
        pass


class Estrategy(BaseKnowledge):
    def __init__(self, knowledge_base: Dict[Knowledge, Any] = None):
        self.knowledge_base = {} if knowledge_base is None else knowledge_base

    def learn(self, data: Dict[Knowledge, Any]):
        for key in data.keys():
            self.knowledge_base[key] = data[key]

    def learn_especific(self, key: Knowledge, data: Any):
        self.knowledge_base[key] = data

    def make_decision(self):
        pass

    def get_knowledge(self, key: Knowledge):
        try:
            return self.knowledge_base[key]
        except KeyError:
            return None
