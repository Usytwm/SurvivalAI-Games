import math
import random
from typing import List, Set, Tuple

from ai.knowledge.knowledge import Fact, Knowledge, Rule
from environment.actions import Action_Info, Action_Type
from environment.sim_object import Sim_Object_Type
from agents.PacifistAgent.tools import move_away_from_attacker


def see_objects_condition(facts: Set[Fact]):
    has_see_objects = any(
        fact.key == Knowledge.SEE_OBJECTS and len(fact.data) > 0 for fact in facts
    )
    has_enemies = any(fact.key == Knowledge.ENEMIES for fact in facts)
    return has_see_objects and has_enemies


def see_objects_action(facts: Set[Fact]):
    see_objects_info = None
    enemies_info = None
    current_pos = None
    possible_moves = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data

    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            if obj.id in enemies_info:
                x_1, y_1 = current_pos
                x_2, y_2 = obj.position
                best_move = move_away_from_attacker(
                    (x_1, y_1), (x_2, y_2), possible_moves
                )
                return [Fact(Knowledge.NEXT_MOVE, best_move)]

    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


def see_actions_condition(facts: Set[Fact]):
    return any(
        fact.key == Knowledge.SEE_ACTIONS and len(fact.data) > 0 for fact in facts
    )


def see_actions_action(facts: Set[Fact]):
    see_actions_info = None
    enemies_info = None
    current_pos = None
    possible_moves = None

    for fact in facts:
        if fact.key == Knowledge.SEE_ACTIONS:
            see_actions_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data

    for action in see_actions_info:
        action = Action_Info(action)
        if action.type == Action_Type.ATTACK:
            id = action.actor_id
            if id in enemies_info:
                x_1, y_1 = current_pos
                x_2, y_2 = action.start_position
                best_move = move_away_from_attacker(
                    current_pos, (x_1 + x_2, y_1 + y_2), possible_moves
                )
                return Fact(Knowledge.NEXT_MOVE, best_move)
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]  # Default move


def move_away_from_attacker_condition(facts: Set[Fact]):
    return any(fact.key == Knowledge.RECEIVED_ATTACK for fact in facts)


def move_away_from_attacker_action(facts: Set[Fact]):
    for fact in facts:
        if fact.key == Knowledge.RECEIVED_ATTACK:
            current_pos = next(
                (f.data for f in facts if f.key == Knowledge.POSITION), None
            )
            possible_moves = next(
                (f.data for f in facts if f.key == Knowledge.POSIBLES_MOVEMENTS), None
            )
            attacker_id, strength, attacker_pos = (
                fact.data
            )  # Assuming data is a tuple with attacker's position as third element
            best_move = move_away_from_attacker(
                current_pos, attacker_pos, possible_moves
            )
            return [Fact(Knowledge.NEXT_MOVE, best_move)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


def default_move_condition(facts: Set[Fact]):
    enemies = set()
    for fact in facts:
        if fact.key == Knowledge.ENEMIES:
            enemies = fact.data
            break

    not_view_objects = all(  # If there are no objects in sight
        fact.key != Knowledge.SEE_OBJECTS
        or len(fact.data) == 0
        or all(not data.id in enemies for data in fact.data)
        for fact in facts
    )
    not_view_actions = all(  # If there are no actions in sight
        fact.key != Knowledge.SEE_ACTIONS or len(fact.data) == 0 for fact in facts
    )
    not_received_attack = all(fact.key != Knowledge.RECEIVED_ATTACK for fact in facts)
    return not_view_objects and not_view_actions and not_received_attack


def default_move_action(facts: Set[Fact]):
    for fact in facts:
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            return [Fact(Knowledge.NEXT_MOVE, random.choice(fact.data))]
    return [Fact(Knowledge.NEXT_MOVE, (0, 0))]


move_away_rule = Rule(move_away_from_attacker_condition, move_away_from_attacker_action)
see_objects_rule = Rule(see_objects_condition, see_objects_action)
see_actions_rule = Rule(see_actions_condition, see_actions_action)
default_move = Rule(default_move_condition, default_move_action)
