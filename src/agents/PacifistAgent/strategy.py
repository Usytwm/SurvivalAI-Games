from typing import Any, Dict
from ai.knowledge.knowledge import (
    BaseKnowledge,
    Fact,
    InferenceEngine,
    Knowledge,
)
from agents.PacifistAgent.Rules import (
    move_away_rule,
    see_objects_rule,
    see_actions_rule,
    default_move,
)


class PacifistEstrategy(BaseKnowledge):
    def __init__(self):
        self.engine = InferenceEngine()
        # Preset knowledge base with initial facts
        self.engine.add_fact(Fact(Knowledge.ALLIES, set()))
        self.engine.add_fact(Fact(Knowledge.ENEMIES, set()))
        self.engine.add_fact(Fact(Knowledge.AGEENTS, set()))
        self.engine.add_fact(Fact(Knowledge.NEXT_MOVE, (0, 0)))

        self.engine.add_rule(move_away_rule)
        self.engine.add_rule(see_objects_rule)
        self.engine.add_rule(see_actions_rule)
        self.engine.add_rule(default_move)

    def learn(self, data: Dict[Knowledge, Any]):
        for key, value in data.items():
            self.engine.add_fact(Fact(key, value))

    def learn_especific(self, key: Knowledge, data: Any):
        self.engine.add_fact(Fact(key, data))

    def make_decision(self):
        # Run the inference engine to get new actions or facts
        new_actions = self.engine.run()
        return new_actions

    def get_knowledge(self, key: Knowledge):
        for fact in self.engine.facts:
            if fact.key == key:
                return fact.data
        return None

    def remove_knowledge(self, key: Knowledge):
        for fact in self.engine.facts:
            if fact.key == key:
                self.engine.remove_fact(fact)

    def remove_all_knowledge(self):
        self.engine.facts = []
