import random
from typing import Set

from ai.knowledge.knowledge import Fact, Knowledge, Rule
from environment.actions import Attack
from environment.sim_object import Sim_Object_Type


def move_condition(facts: Set[Fact]):
    return any(
        fact.key == Knowledge.POSIBLES_MOVEMENTS and len(fact.data) > 0
        for fact in facts
    )


def move_action(facts: Set[Fact]):
    possible_moves = None
    for fact in facts:
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


def get_attacks_condition(facts: Set[Fact]):
    objects = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            objects = fact.data

    return any(
        obj.type.value == Sim_Object_Type.AGENT.value for obj in objects
    ) and random.choice([True, False])


def get_attacks_action(facts: Set[Fact]):
    objects = None
    current_id = None
    resource = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            objects = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            resource = fact.data

    count_agents = len(
        list(filter(lambda x: x.type.value == Sim_Object_Type.AGENT.value, objects))
    )
    streght_for_agent = resource // count_agents
    all_atacks = []
    for obj in objects:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            attack = Attack(
                current_id,
                obj.id,
                random.randint(0, streght_for_agent),
            )
            all_atacks.append(attack)

    count_all_attacks = len(all_atacks)
    count_attack = random.randint(0, count_all_attacks)
    atacks = random.sample(all_atacks, count_attack)
    return [Fact(Knowledge.GETATTACKS, atacks)]


move_rule = Rule(move_condition, move_action)
attack_rule = Rule(get_attacks_condition, get_attacks_action)
