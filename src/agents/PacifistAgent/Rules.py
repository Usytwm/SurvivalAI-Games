import math
import random
from typing import List, Set, Tuple

from ai.knowledge.knowledge import Fact, Knowledge, Rule
from ai.search.bfs import BFS
from environment.actions import Action_Info, Action_Type
from environment.sim_object import Agent_Info, Sim_Object_Type
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
    geography = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data

    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            if obj.id in enemies_info:
                bfs = BFS(geography.validate_position)
                obstacles = [
                    obj.position
                    for obj in see_objects_info
                    if obj.type.value == 1 and isinstance(obj, Agent_Info)
                ]
                obstacles = [
                    (obstacle[0] + current_pos[0], obstacle[1] + current_pos[1])
                    for obstacle in obstacles
                ]
                bfs.set_obstacles(obstacles)
                goal_position = (
                    obj.position[0] + current_pos[0],
                    obj.position[1] + current_pos[1],
                )
                path = bfs.bfs_path(current_pos, goal_position)
                relative_pos = (path[0] - current_pos[0], path[1] - current_pos[1])
                if path:
                    return [Fact(Knowledge.NEXT_MOVE, relative_pos)]

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
    geography = None
    see_objects_info = None
    for fact in facts:
        if fact.key == Knowledge.SEE_ACTIONS:
            see_actions_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data

    for action in see_actions_info:
        action = action
        if action.type == Action_Type.ATTACK:
            id = action.actor_id
            if id in enemies_info:
                bfs = BFS(geography.validate_position)
                obstacles = [
                    obj.position for obj in see_objects_info if obj.type.value == 1
                ]
                obstacles = [
                    (obstacle[0] + current_pos[0], obstacle[1] + current_pos[1])
                    for obstacle in obstacles
                ]
                bfs.set_obstacles(obstacles)
                goal_position = (
                    action.position[0] + current_pos[0],
                    action.position[1] + current_pos[1],
                )
                path = bfs.bfs_path(current_pos, goal_position)
                relative_pos = (path[0] - current_pos[0], path[1] - current_pos[1])
                if path:
                    return [Fact(Knowledge.NEXT_MOVE, relative_pos)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]  # Default move


def move_away_from_attacker_condition(facts: Set[Fact]):
    return any(fact.key == Knowledge.RECEIVED_ATTACK and fact.data for fact in facts)


def move_away_from_attacker_action(facts: Set[Fact]):
    geography = None
    current_pos = None
    possible_moves = None
    see_objects_info = None
    atack_data = None
    attacker_id, strength, attacker_pos = None, None, None
    for fact in facts:
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data
        if fact.key == Knowledge.RECEIVED_ATTACK:
            atack_data = (
                fact.data
            )  # Assuming data is a tuple with attacker's position as third element
            attacker_id, strength, attacker_pos = atack_data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data

    bfs = BFS(geography.validate_position)
    obstacles = [obj.position for obj in see_objects_info if obj.type.value == 1]
    obstacles = [
        (obstacle[0] + current_pos[0], obstacle[1] + current_pos[1])
        for obstacle in obstacles
    ]
    bfs.set_obstacles(obstacles)
    path = bfs.bfs_path(current_pos, attacker_pos)
    relative_pos = (path[0] - current_pos[0], path[1] - current_pos[1])
    for fact in facts:
        if fact.key == Knowledge.RECEIVED_ATTACK:
            fact.data = None
    if path:
        return [Fact(Knowledge.NEXT_MOVE, relative_pos)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


def default_move_condition_pasific(facts: Set[Fact]):
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
    not_received_attack = all(
        fact.key != Knowledge.RECEIVED_ATTACK for fact in facts
    ) or any(
        fact.key == Knowledge.RECEIVED_ATTACK and fact.data == None for fact in facts
    )
    return not_view_objects and not_view_actions and not_received_attack


def default_move_action_pasific(facts: Set[Fact]):
    for fact in facts:
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            return [Fact(Knowledge.NEXT_MOVE, random.choice(fact.data))]
    return [Fact(Knowledge.NEXT_MOVE, (0, 0))]


move_away_rule = Rule(move_away_from_attacker_condition, move_away_from_attacker_action)
see_objects_rule = Rule(see_objects_condition, see_objects_action)
see_actions_rule = Rule(see_actions_condition, see_actions_action)
default_move = Rule(default_move_condition_pasific, default_move_action_pasific)
