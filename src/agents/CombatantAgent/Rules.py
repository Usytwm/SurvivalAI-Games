import random
from typing import Set
from agents.PacifistAgent.tools import move_away_from_attacker
from ai.knowledge.knowledge import Fact, Knowledge, Rule
from ai.search.bfs import BFS
from ai.search.pathFinder_with_Astar import PathFinder
from environment.actions import Association_Proposal, Attack
from environment.sim_object import Agent_Info, Sim_Object_Type


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
    current_pos = None
    geography = None
    for fact in facts:
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            strength = int(fact.data)
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data

    # strength_to_attack = strength / len(enemies_info) if len(enemies_info) > 0 else 1
    # atacaral que menos reserva tenga
    # min_enemy = min(enemies_info, key=lambda x: x.resources)
    agents_enemies = [
        obj
        for obj in see_objects_info
        if isinstance(obj, Agent_Info)
        and obj.type.value == Sim_Object_Type.AGENT.value
        and obj.id in enemies_info
    ]
    min_enemy = min(agents_enemies, key=lambda x: x.resources)
    if min_enemy.resources > strength:
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
            min_enemy.position[0] + current_pos[0],
            min_enemy.position[1] + current_pos[1],
        )
        path = bfs.bfs_path(current_pos, goal_position)
        relative_pos = (path[0] - current_pos[0], path[1] - current_pos[1])
        if path:
            return [Fact(Knowledge.NEXT_MOVE, relative_pos)]
    attack = Attack(
        current_id, min_enemy.id, random.randint(0, min_enemy.resources + 1)
    )

    return [
        Fact(Knowledge.GETATTACKS, [attack]),
    ]


# *Hay agentes en mi campo de vision y ninguno es mi enemigo, lo ataco y me muevo
def to_attack_not_enemy_condition(facts: Set[Fact]):
    see_objects_info = None
    enemies_info = None

    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies_info = fact.data

    posibles_positions = any(
        fact.key == Knowledge.POSIBLES_MOVEMENTS and len(fact.data) > 0
        for fact in facts
    )

    has_agents = any(
        obj.type.value == Sim_Object_Type.AGENT.value for obj in see_objects_info
    )

    not_enemy = all(
        obj.id not in enemies_info
        for obj in see_objects_info
        if obj.type.value == Sim_Object_Type.AGENT.value
    )

    return has_agents and not_enemy and posibles_positions


# *OK
def to_attack_not_enemy_action(facts: Set[Fact]):
    see_objects_info = None
    current_id = None
    agents_ = None
    current_pos = None
    strength = 1
    see_resource_info = None
    geography = None
    getattacs = []
    next_move_relative = None
    for fact in facts:
        if fact.key == Knowledge.SEE_OBJECTS:
            see_objects_info = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.RESERVE:
            strength = int(fact.data)
        if fact.key == Knowledge.POSITION:
            current_pos = fact.data
        if fact.key == Knowledge.POSIBLES_MOVEMENTS:
            possible_moves = fact.data
        if fact.key == Knowledge.SEE_RESOURCES:
            see_resource_info = fact.data
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
        if next_move:
            next_move_relative = (next_move[0] - start[0], next_move[1] - start[1])
            # return [Fact(Knowledge.NEXT_MOVE, next_move_relative)]
    # return [Fact(Knowledge.NEXT_MOVE, random.choice(possible_moves))]

    agents_ = [
        obj
        for obj in see_objects_info
        if obj.type.value == Sim_Object_Type.AGENT.value and isinstance(obj, Agent_Info)
    ]
    strength_to_attack = strength / len(agents_) if len(agents_) > 0 else 1

    for obj in agents_:
        attack = Attack(current_id, obj.id, random.randint(0, strength_to_attack // 4))
        getattacs.append(attack)

    return [
        Fact(Knowledge.GETATTACKS, getattacs),
        Fact(Knowledge.NEXT_MOVE, next_move_relative),
    ]


# * Hay un agente en mi campo de vision que me ataca
def recived_attacker_condition(facts: Set[Fact]):
    return any(fact.key == Knowledge.RECEIVED_ATTACK and fact.data for fact in facts)


# *OK
def recived_attacker_action(facts: Set[Fact]):
    geography = None
    current_pos = None
    possible_moves = None
    see_objects_info = None
    atack_data = None
    attacker_id, strength, attacker_pos = None, None, None
    reserve = None
    current_id = None
    for fact in facts:
        if fact.key == Knowledge.GEOGRAPHIC_MEMORY:
            geography = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
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
        if fact.key == Knowledge.RESERVE:
            reserve = int(fact.data)

    attack_strength = strength * 2 if reserve > strength * 3 else reserve - strength
    if attack_strength < 0:
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
    else:
        attack = Attack(current_id, attacker_id, attack_strength)
        for fact in facts:
            if fact.key == Knowledge.RECEIVED_ATTACK:
                fact.data = None
        return [Fact(Knowledge.GETATTACKS, [attack])]


# !si hay varios enemigos cercanos y no tengo mucha azucar como para atacra o recibir los ataques de todos decido aliarme con alguno
def association_proposal_condition(facts: Set[Fact]):
    # Evaluar condiciones de asociación
    has_two_enemy = any(
        fact.key == Knowledge.ENEMIES and len(fact.data) > 1 for fact in facts
    )

    enemies = None
    reserve = None
    objects_info = None
    enemies_in_view: list[Agent_Info] = []
    for fact in facts:
        if fact.key == Knowledge.RESERVE:
            reserve = fact.data
        if fact.key == Knowledge.ENEMIES:
            enemies = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            objects_info = fact.data

    has_agent_not_enemy = any(
        fact.key == Knowledge.SEE_OBJECTS
        and any(
            isinstance(obj, Agent_Info)
            and obj.type.value == Sim_Object_Type.AGENT.value
            and obj.id not in enemies
            for obj in fact.data
        )
        for fact in facts
    )

    for obj in objects_info:
        if (
            isinstance(obj, Agent_Info)
            and obj.type.value == Sim_Object_Type.AGENT.value
            and obj.id in enemies
        ):
            enemies_in_view.append(obj)

    return (
        has_two_enemy
        and has_agent_not_enemy
        and reserve < sum([enemy.resources for enemy in enemies_in_view])
    )


def association_proposal_action(facts: Set[Fact]):
    not_enemies: list[Agent_Info] = []
    enemies = None
    current_id = None
    objects_info = None
    asociation = None
    for fact in facts:
        if fact.key == Knowledge.ENEMIES:
            enemies = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            objects_info = fact.data
        if fact.key == Knowledge.ID:
            current_id = fact.data
        if fact.key == Knowledge.ASSOCIATION:
            asociation = fact.data
    agents_associated = set()
    for asoc in asociation.values():
        agents_associated.update(asoc.members)

    if current_id in agents_associated:
        agents_associated.remove(current_id)

    for obj in objects_info:
        if (
            isinstance(obj, Agent_Info)
            and obj.type.value == Sim_Object_Type.AGENT.value
            and obj.id not in enemies
            and obj.id not in agents_associated
        ):
            not_enemies.append(obj)
    selected_agent_max_resources = (
        max(not_enemies, key=lambda x: x.resources) if not_enemies else None
    )
    if not selected_agent_max_resources:
        return []
    commitments = {}
    commitments[current_id] = (0.2, 0.5)
    commitments[selected_agent_max_resources.id] = (0.2, 0.5)
    proposal = Association_Proposal(
        current_id, [current_id, selected_agent_max_resources.id], commitments
    )

    return [Fact(Knowledge.GETASSOCIATIONPROPOSALS, [proposal])]


def recived_proposal_condition(facts: Set[Fact]):
    return any(
        fact.key == Knowledge.ASSOCIATION_PROPOSALS and fact.data for fact in facts
    )


def recived_proposal_action(facts: Set[Fact]):
    association_proposal = None
    objects_info = None
    actor = None
    resources = None
    for fact in facts:
        if fact.key == Knowledge.ASSOCIATION_PROPOSALS:
            association_proposal = fact.data
        if fact.key == Knowledge.SEE_OBJECTS:
            objects_info = fact.data
        if fact.key == Knowledge.RESERVE:
            resources = fact.data
    actor_id = association_proposal.members[1]
    for obj in objects_info:
        if isinstance(obj, Agent_Info) and obj.id == actor_id:
            actor = obj
            break
    if actor:
        return [
            Fact(
                Knowledge.CONSIDER_ASSOCIATION_PROPOSAL,
                actor.resources > resources // 2,
            )
        ]
    return [Fact(Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, random.choice([True, False]))]


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


association_proposal_rule = Rule(
    association_proposal_condition, association_proposal_action
)

recived_association_proposal_rule = Rule(
    recived_proposal_condition, recived_proposal_action
)


attack_enemy_in_vision = Rule(to_attack_enemy_condition, to_attack_enemy_action)

attack_not_enemy_in_vision = Rule(
    to_attack_not_enemy_condition, to_attack_not_enemy_action
)

move_not_enemy = Rule(to_attack_not_enemy_condition, to_eat_not_view_agents_action)

recived_attacker = Rule(recived_attacker_condition, recived_attacker_action)

default_move = Rule(default_move_condition, default_move_action)
