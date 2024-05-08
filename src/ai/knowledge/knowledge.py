from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict
from typing import Any, Dict, Set, List, Callable


class Knowledge(Enum):
    POSITION = "position"
    RESERVE = "reserve"
    HEALTH = "health"
    GETATTACKS = "getattacks"
    GETASSOCIATIONPROPOSALS = "getassociationproposals"
    ASSOCIATION_PROPOSALS = "association_proposals"
    CONSIDER_ASSOCIATION_PROPOSAL = "consider_association_proposal"
    ASSOSIATION_MEMORY = "association_memory"
    ASSOCIATION = "association"
    ATTACK_MADE = "attack_made"
    RECEIVED_ATTACK = "received_attack"
    ATTACK_REWARD = "attack_reward"
    SEE_OBJECTS = "see_objects"
    SEE_RESOURCES = "see_resources"
    SEE_ACTIONS = "see_actions"
    FEED = "feed"
    BURN = "burn"
    ID = "id"
    POSIBLES_MOVEMENTS = "posibles_movements"
    ALLIES = "allies"
    ENEMIES = "enemies"
    AGEENTS = "agents"
    NEXT_MOVE = "next_move"
    PREVPOSSITION = "prevposition"
    GEOGRAPHIC_MEMORY = "geographic_memory"
    MEMORY_FOR_AGENTS_SIGHTS = "memory_for_agents_sights"
    MEMORY_FOR_ATTACKS = "memory_for_attacks"
    BEHAVIOR = "behavior"


class Fact:
    def __init__(self, key: Knowledge, data: Any):
        self.key = key
        self.data = data

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return (
            isinstance(other, Fact)
            and self.key.value == other.key.value
            and self.data == other.data
        )

    def __repr__(self):
        return f"Fact({self.key.name}, {self.data})"


class Rule:
    def __init__(
        self,
        condition: Callable[[Set[Fact]], bool],
        action: Callable[[Set[Fact]], List[Fact]],
    ):
        self.condition = condition
        self.action = action

    def evaluate(self, facts: Set[Fact]) -> List[Fact]:
        if self.condition(facts):
            return self.action(facts)
        return []


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
    def __init__(self, initial_facts: List[Fact] = [], initial_rules: List[Rule] = []):
        self.engine = InferenceEngine()
        for fact in initial_facts:
            self.engine.add_fact(fact)
        for rule in initial_rules:
            self.engine.add_rule(rule)

    def learn(self, data: Dict[Knowledge, Any]):
        for key, value in data.items():
            self.engine.add_fact(Fact(key, value))

    def learn_especific(self, key: Knowledge, data: Any):
        self.engine.add_fact(Fact(key, data))

    def make_decision(self):
        new_actions = self.engine.run()
        return new_actions

    def get_knowledge(self, key: Knowledge):
        for fact in self.engine.facts:
            if fact.key == key:
                return fact.data
        return None

    def remove_knowledge(self, key: Knowledge):
        to_remove = [fact for fact in self.engine.facts if fact.key == key]
        for fact in to_remove:
            self.engine.remove_fact(fact)

    def remove_all_knowledge(self):
        self.engine.facts = []


class InferenceEngine:
    def __init__(self):
        self.facts: Set[Fact] = set()
        self.rules: List[Rule] = []

    def add_fact(self, fact: Fact):
        self.facts = {f for f in self.facts if f.key != fact.key}
        self.facts.add(fact)

    def add_facts(self, facts: List[Fact]):
        for fact in facts:
            self.add_fact(fact)

    def remove_fact(self, fact: Fact):
        self.facts.discard(fact)

    def remove_all_facts(self):
        self.facts = set()

    def add_rules(self, rules: List[Rule]):
        for rule in rules:
            self.add_rule(rule)

    def add_rule(self, rule: Rule):
        if not rule in self.rules:
            self.rules.append(rule)
        # self.rules.append(rule)

    def remove_rule(self, rule: Rule):
        self.rules.remove(rule)

    def remove_all_rules(self):
        self.rules = []

    def run(self) -> List[Fact]:
        new_facts: Set[Fact] = set()
        for rule in self.rules:
            results = rule.evaluate(self.facts)
            new_facts.update(results)
        temp_facts = {fact.key: fact for fact in self.facts}
        for new_fact in new_facts:
            temp_facts[new_fact.key] = new_fact
        self.facts = set(temp_facts.values())
        return list(self.facts)
        # new_facts = set()
        # for rule in self.rules:
        #     results = rule.evaluate(self.facts)
        #     new_facts.update(results)
        # self.facts.update(new_facts)
        # return list(new_facts)
