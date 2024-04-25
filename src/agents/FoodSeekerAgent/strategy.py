from typing import Any, Dict
from ai.knowledge.knowledge import (
    Estrategy,
    Fact,
    Knowledge,
)


class FoodSeekerEstrategy(Estrategy):
    def __init__(self):
        super().__init__()
        # Preset knowledge base with initial facts
        self.engine.add_fact(Fact(Knowledge.ALLIES, set()))
        self.engine.add_fact(Fact(Knowledge.ENEMIES, set()))
        self.engine.add_fact(Fact(Knowledge.AGEENTS, set()))
        self.engine.add_fact(Fact(Knowledge.NEXT_MOVE, (0, 0)))

        # self.engine.add_rule(move_away_rule)
        # self.engine.add_rule(see_objects_rule)
        # self.engine.add_rule(see_actions_rule)
        # self.engine.add_rule(default_move)
