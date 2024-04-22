from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict


class Keys(Enum):
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
    def __init__(self, knowledge_base: Dict[Keys, Any] = None):
        self.knowledge_base = {} if knowledge_base is None else knowledge_base

    @abstractmethod
    def learn(self, data: Dict[Keys, Any]):
        """
        Aprende del entorno o de los datos proporcionados.
        """
        pass

    @abstractmethod
    def learn_especific(self, key: Keys, data: Any):
        """
        Aprende del entorno.
        """
        pass

    @abstractmethod
    def make_decision(self):
        """
        Toma una decisión basada en la base de conocimientos actual.
        """
        pass
