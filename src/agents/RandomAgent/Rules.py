import random
from typing import Set

from ai.knowledge.knowledge import Fact, Knowledge, Rule
from environment.actions import Association_Proposal, Attack
from environment.sim_object import Agent_Info, Sim_Object_Type


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
    asociation = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            objects = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            resource = fact.data
        if fact.key == Knowledge.ASSOCIATION:
            asociation = fact.data

    agents_associated = set()
    for asoc in asociation.values():
        agents_associated.update(asoc.members)

    if current_id in agents_associated:
        agents_associated.remove(current_id)

    count_agents = len(
        list(
            filter(
                lambda x: isinstance(x, Agent_Info)
                and x.type.value == Sim_Object_Type.AGENT.value
                and x.id not in agents_associated,
                objects,
            )
        )
    )
    streght_for_agent = (resource // count_agents) if count_agents > 0 else 0
    all_atacks = []
    for obj in objects:
        if (
            isinstance(obj, Agent_Info)
            and obj.type.value == Sim_Object_Type.AGENT.value
            and obj.id not in agents_associated
        ):
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


def recived_proposal_condition_random(facts: Set[Fact]):
    return any(
        fact.key == Knowledge.ASSOCIATION_PROPOSALS and fact.data for fact in facts
    )


def recived_proposal_action_random(facts: Set[Fact]):

    return [Fact(Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, random.choice([True, False]))]


def propose_association_condition(facts: Set[Fact]):
    # Randomly decide to propose an association 10% of the time when there are other agents visible
    see_agents = any(
        fact.key == Knowledge.SEE_OBJECTS
        and any(obj.type.value == Sim_Object_Type.AGENT.value for obj in fact.data)
        for fact in facts
    )
    return (
        see_agents and random.random() < 0.1
    )  # 10% chance !verificar que no tenga ninguna alianza ya


def propose_association_action(facts: Set[Fact]):
    self_id = None
    enemies = []
    current_id = None
    for fact in facts:
        if fact.key == Knowledge.ID:
            self_id = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies = fact.data
        if fact.key == Knowledge.ASSOCIATION:
            asociation = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data

    agents_associated = set()
    for asoc in asociation.values():
        agents_associated.update(asoc.members)

    if current_id in agents_associated:
        agents_associated.remove(current_id)
    agents_seen = [
        obj
        for fact in facts
        if fact.key == Knowledge.SEE_OBJECTS
        for obj in fact.data
        if obj.type.value == Sim_Object_Type.AGENT.value
        and isinstance(obj, Agent_Info)
        and obj.id not in enemies
        and obj.id not in agents_associated
    ]
    proposals = []
    if agents_seen:
        selected_agent = random.choice(agents_seen)
        commitments = {}
        commitments[self_id] = (0.2, 0.5)
        commitments[selected_agent.id] = (0.2, 0.5)
        proposal = Association_Proposal(
            self_id, [self_id, selected_agent.id], commitments
        )
        proposals.append(proposal)
    return [Fact(Knowledge.GETASSOCIATIONPROPOSALS, proposals)]


association_propose_rule = Rule(
    propose_association_condition, propose_association_action
)
recived_association_propose_rule = Rule(
    recived_proposal_condition_random, recived_proposal_action_random
)
move_rule = Rule(move_condition, move_action)
attack_rule = Rule(get_attacks_condition, get_attacks_action)
