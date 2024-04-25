import random
from typing import Set
from agents.PacifistAgent.tools import move_away_from_attacker
from ai.knowledge.knowledge import Fact, Knowledge, Rule
from environment.actions import Attack
from environment.sim_object import Sim_Object_Type

import heapq


class PathFinder:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pass

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start, goal, movements):
        open_heap = []
        heapq.heappush(open_heap, (0 + self.heuristic(start, goal), 0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while open_heap:
            _, current_cost, current = heapq.heappop(open_heap)

            if current == goal:
                return self.reconstruct_path(came_from, start, goal)

            for move in movements:
                if move == (0, 0):
                    continue  # Ignore the non-moving option in pathfinding
                next = (current[0] + move[0], current[1] + move[1])
                if 0 <= next[0] < self.width and 0 <= next[1] < self.height:
                    new_cost = current_cost + 1  # Assuming all moves have the same cost
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.heuristic(next, goal)
                        heapq.heappush(open_heap, (priority, new_cost, next))
                        came_from[next] = current

        return None  # No path found

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path


def to_eat_not_enemies_condition(facts: Set[Fact]):
    has_see_resource = any(
        fact.key == Knowledge.SEE_RESOURCES and len(fact.data) > 0 for fact in facts
    )
    posibles_positions = any(
        fact.key == Knowledge.POSIBLES_MOVEMENTS and len(fact.data) > 0
        for fact in facts
    )
    see_objects_info = []
    enemies_info = []
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data

    # Verificar que no haya enemigos en el campo de visión
    no_enemies_in_view = all(
        obj.id not in enemies_info
        for obj in see_objects_info
        if obj.type.value == Sim_Object_Type.AGENT.value
    )
    return has_see_resource and posibles_positions and no_enemies_in_view


def to_eat_not_enemies_action(facts: Set[Fact]):
    see_resource_info = None
    current_pos = None
    possible_moves = None
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
    start = current_pos
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(10, 10)
    path = finder.a_star(start, goal, possible_moves)
    if path:
        if len(path) > 1:
            next_move = path[1]
        else:
            next_move = path[0]
        next_move_relative = (next_move[0] - start[0], next_move[1] - start[1])
        if next_move:
            return [Fact(Knowledge.NEXT_MOVE, next_move_relative)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


def to_eat_enemy_condition(facts: Set[Fact]):
    has_see_resource = any(
        fact.key == Knowledge.SEE_RESOURCES and len(fact.data) > 0 for fact in facts
    )
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

    return has_see_resource and has_enemies and only_enemy


def to_eat_enemy_action(facts: Set[Fact]):
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

    for obj in see_objects_info:
        if obj.type.value == Sim_Object_Type.AGENT.value:
            if obj.id in enemies_info:
                attack = Attack(current_id, obj.id, strength)
                getattacs.append(attack)

    return [
        Fact(Knowledge.GETATTACKS, getattacs),
    ]


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
    for fact in facts:
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
    start = current_pos
    goal_relative = max(see_resource_info, key=lambda x: x[1])[0]
    goal = (start[0] + goal_relative[0], start[1] + goal_relative[1])
    finder = PathFinder(10, 10)
    path = finder.a_star(start, goal, possible_moves)
    if path:
        if len(path) > 1:
            next_move = path[1]
        else:
            next_move = path[0]
        next_move_relative = (next_move[0] - start[0], next_move[1] - start[1])
        if next_move:
            return [Fact(Knowledge.NEXT_MOVE, next_move_relative)]
    return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]


eat_not_enemy_rule = Rule(to_eat_not_enemies_condition, to_eat_not_enemies_action)
eat_enemy_rule = Rule(to_eat_enemy_condition, to_eat_enemy_action)
default_move_rule = Rule(default_move_condition, default_move_action)
