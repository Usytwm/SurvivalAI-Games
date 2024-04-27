import random
from typing import Set
from agents.PacifistAgent.tools import move_away_from_attacker
from ai.knowledge.knowledge import Fact, Knowledge, Rule
from ai.search.pathFinder_with_Astar import PathFinder
from environment.actions import Attack
from environment.sim_object import Sim_Object_Type

import heapq


# *OK no hay agentes en mi camo de vision y hay recursos parta aumentar mi fuerza de ataque
def to_eat_not_view_agents_condition(facts: Set[Fact]):
    has_see_resource = any(
        fact.key == Knowledge.SEE_RESOURCES and len(fact.data) > 0 for fact in facts
    )
    posibles_positions = any(
        fact.key == Knowledge.POSIBLES_MOVEMENTS and len(fact.data) > 0
        for fact in facts
    )
    see_objects_info = []
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data

    # Verificar que no haya agentes en el campo de visión
    no_gents_in_view = all(
        obj.type.value != Sim_Object_Type.AGENT.value for obj in see_objects_info
    )

    return has_see_resource and posibles_positions and no_gents_in_view


# *OK
def to_eat_not_view_agents_action(facts: Set[Fact]):
    see_resource_info = None
    current_pos = None
    possible_moves = None
    see_objects_info = None
    geography = None
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data
    start = current_pos
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(geography.validate_position)
    obstacles = [obj.position for obj in see_objects_info]
    obstacles = [
        (obstacle[0] + current_pos[0], obstacle[1] + current_pos[1])
        for obstacle in obstacles
    ]
    finder.set_obstacles(obstacles)
    path = finder.a_star(start, goal)
    if path:
        if len(path) > 1:
            next_move = path[1]
        else:
            next_move = path[0]
        next_move_relative = (next_move[0] - start[0], next_move[1] - start[1])
        if next_move:
            return [Fact(Knowledge.NEXT_MOVE, next_move_relative)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


# *Hay agentes en mi campo de vision y alguno es enemigo mio
def to_attack_enemy_condition(facts: Set[Fact]):
    has_enemies = any(
        fact.key == Knowledge.ENEMIES and len(fact.data) > 0 for fact in facts
    )
    see_objects_info = None
    enemies_info = None

    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data

    only_enemy = False
    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            if obj.id in enemies_info:
                only_enemy = True
                break

    return has_enemies and only_enemy


# *OK
def to_attack_enemy_action(facts: Set[Fact]):
    see_objects_info = None
    enemies_info = None
    current_id = None
    strength = 1
    getattacs = []
    for fact in facts:
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            strength = int(fact.data)

    strength_to_attack = strength / len(enemies_info) if len(enemies_info) > 0 else 1

    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            if obj.id in enemies_info:
                attack = Attack(
                    current_id, obj.id, random.randint(0, strength_to_attack // 2)
                )
                getattacs.append(attack)

    return [
        Fact(Knowledge.GETATTACKS, getattacs),
    ]


# *Hay agentes en mi campo de vision y ninguno es mi enemigo
def to_attack_not_enemy_condition(facts: Set[Fact]):
    has_enemies = any(
        fact.key == Knowledge.ENEMIES and len(fact.data) > 0 for fact in facts
    )
    see_objects_info = None
    enemies_info = None

    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data

    has_agents = any(
        obj.type.value == Sim_Object_Type.AGENT.value for obj in see_objects_info
    )

    not_enemy = all(
        obj.id not in enemies_info
        for obj in see_objects_info
        if obj.type.value == Sim_Object_Type.AGENT.value
    )

    return has_enemies and has_agents and not_enemy


# *OK
def to_attack_not_enemy_action(facts: Set[Fact]):
    see_objects_info = None
    current_id = None
    agents_ = None
    strength = 1
    getattacs = []
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            strength = int(fact.data)

    agents_ = [
        obj for obj in see_objects_info if obj.type.value == Sim_Object_Type.AGENT.value
    ]
    strength_to_attack = strength / len(agents_) if len(agents_) > 0 else 1

    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            attack = Attack(
                current_id, obj.id, random.randint(0, strength_to_attack // 4)
            )
            getattacs.append(attack)

    return [
        Fact(Knowledge.GETATTACKS, getattacs),
    ]


def stuck_and_resources_available_condition(facts: Set[Fact]):
    prev_position = None
    current_position = None
    see_objects_info = None
    objects_in_path = []
    see_resource_info = None
    geography = None
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.PREVPOSSITION:
            prev_position = fact.data
        if fact.key == Knowledge.POSITION:
            current_position = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data

    start = current_position
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(geography.validate_position)
    obstacles = [obj.position for obj in see_objects_info if obj.type.value == 1]
    obstacles = [
        (obstacle[0] + current_position[0], obstacle[1] + current_position[1])
        for obstacle in obstacles
    ]
    finder.set_obstacles(obstacles)
    path = finder.a_star(start, goal)
    if path:
        for position in path:
            for j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for obj in see_objects_info:
                    position_in_path = (position[0] + j[0], position[1] + j[1])
                    position_object = (
                        obj.position[0] + current_position[0],
                        obj.position[1] + current_position[1],
                    )
                    if position_in_path == position_object:
                        objects_in_path.append(obj)

    return prev_position == current_position and len(objects_in_path) > 0


def stuck_and_resources_available_action(facts: Set[Fact]):
    current_position = None
    see_objects_info = None
    objects_in_path = []
    see_resource_info = None
    get_attacks_currents = []
    strength = 1
    current_id = None
    geography = None
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_position = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        # if fact.key == Knowledge.GETATTACKS:
        #     get_attacks_currents = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            strength = int(fact.data)
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data

    start = current_position
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(geography.validate_position)
    obstacles = [obj.position for obj in see_objects_info if obj.type.value == 1]
    obstacles = [
        (obstacle[0] + current_position[0], obstacle[1] + current_position[1])
        for obstacle in obstacles
    ]
    finder.set_obstacles(obstacles)
    path = finder.a_star(start, goal)
    if path:
        for position in path:
            for j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for obj in see_objects_info:
                    position_in_path = (position[0] + j[0], position[1] + j[1])
                    position_object = (
                        obj.position[0] + current_position[0],
                        obj.position[1] + current_position[1],
                    )
                    if position_in_path == position_object:
                        objects_in_path.append(obj)

    for obj in objects_in_path:
        attack = Attack(current_id, obj.id, random.randint(0, strength // 2))
        get_attacks_currents.append(attack)

    return (Fact(Knowledge.GETATTACKS, get_attacks_currents),)


def default_move_condition(facts: Set[Fact]):
    has_see_resource = any(
        fact.key == Knowledge.SEE_RESOURCES and len(fact.data) > 0 for fact in facts
    )
    posibles_positions = any(
        fact.key == Knowledge.POSIBLES_MOVEMENTS and len(fact.data) > 0
        for fact in facts
    )
    not_view_objects = all(  # If there are no objects in sight
        fact.key != Knowledge.SEE_OBJECTS or len(fact.data) == 0 for fact in facts
    )

    return has_see_resource and posibles_positions and not_view_objects


def default_move_action(facts: Set[Fact]):
    see_resource_info = None
    current_pos = None
    possible_moves = None
    geography = None
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data
    start = current_pos
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(geography.validate_position)
    path = finder.a_star(start, goal)
    if path:
        if len(path) > 1:
            next_move = path[1]
        else:
            next_move = path[0]
        next_move_relative = (next_move[0] - start[0], next_move[1] - start[1])
        if next_move:
            return [Fact(Knowledge.NEXT_MOVE, next_move_relative)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


eat_not_agents_rule = Rule(
    to_eat_not_view_agents_condition, to_eat_not_view_agents_action
)


#! This rule is not used in the current implementation
