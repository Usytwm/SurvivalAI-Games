# *OK no hay agentes en mi camo de vision y hay recursos parta aumentar mi fuerza de ataque
from typing import Set
from agents.CombatantAgent.Rules import (
    recived_attacker_action,
    recived_attacker_condition,
    recived_proposal_action,
    recived_proposal_condition,
    to_attack_enemy_action,
    to_attack_enemy_condition,
    to_attack_not_enemy_action,
    to_attack_not_enemy_condition,
    to_eat_not_view_agents_action,
    to_eat_not_view_agents_condition,
    association_proposal_condition,
    association_proposal_action,
    default_move_condition,
    default_move_action,
)
from agents.FoodSeekerAgent.Rules import (
    default_move_action_foodSeker,
    default_move_condition_foodSeker,
    stuck_and_resources_available_action,
    stuck_and_resources_available_condition,
    to_eat_enemy_action,
    to_eat_enemy_condition,
    to_eat_not_enemies_action,
    to_eat_not_enemies_condition,
)
from agents.PacifistAgent.Rules import (
    default_move_action_pasific,
    default_move_condition_pasific,
    move_away_from_attacker_action,
    move_away_from_attacker_condition,
    see_actions_action,
    see_actions_condition,
    see_objects_action,
    see_objects_condition,
)
from agents.RandomAgent.Rules import (
    get_attacks_action,
    get_attacks_condition,
    move_action,
    move_condition,
    propose_association_action,
    propose_association_condition,
    recived_proposal_action_random,
    recived_proposal_condition_random,
)
from ai.knowledge.knowledge import Fact, Knowledge, Rule


# ? Reglas de experto
# ! REGLAS PARA AGENTE DE COMBATE

combatant_eat_not_agents_rule = Rule(
    to_eat_not_view_agents_condition, to_eat_not_view_agents_action
)


combatant_association_proposal_rule = Rule(
    association_proposal_condition, association_proposal_action
)

combatant_recived_association_proposal_rule = Rule(
    recived_proposal_condition, recived_proposal_action
)


combatant_attack_enemy_in_vision = Rule(
    to_attack_enemy_condition, to_attack_enemy_action
)

combatant_attack_not_enemy_in_vision = Rule(
    to_attack_not_enemy_condition, to_attack_not_enemy_action
)

combatant_move_not_enemy = Rule(
    to_attack_not_enemy_condition, to_eat_not_view_agents_action
)

combatant_recived_attacker = Rule(recived_attacker_condition, recived_attacker_action)

combatant_default_move = Rule(default_move_condition, default_move_action)


# !REGLAS PARA AGENTE PACIFISTA

pasific_move_away_rule = Rule(
    move_away_from_attacker_condition, move_away_from_attacker_action
)
pasific_see_objects_rule = Rule(see_objects_condition, see_objects_action)
pasific_see_actions_rule = Rule(see_actions_condition, see_actions_action)
pasific_default_move = Rule(default_move_condition_pasific, default_move_action_pasific)

# !REGLAS PARA AGENTE BUSCADOR DE RECURSOS

food_seeker_association_proposal_rule = Rule(
    association_proposal_condition, association_proposal_action
)

food_seeker_eat_not_enemy_rule = Rule(
    to_eat_not_enemies_condition, to_eat_not_enemies_action
)
food_seeker_eat_enemy_rule = Rule(to_eat_enemy_condition, to_eat_enemy_action)
food_seeker_stuck_and_resources_available_rule = Rule(
    stuck_and_resources_available_condition, stuck_and_resources_available_action
)
food_seeker_default_move_rule = Rule(
    default_move_condition_foodSeker, default_move_action_foodSeker
)

# !REGLAS PARA AGENTE RANDOM

random_association_propose_rule = Rule(
    propose_association_condition, propose_association_action
)
random_recived_association_propose_rule = Rule(
    recived_proposal_condition_random, recived_proposal_action_random
)
random_move_rule = Rule(move_condition, move_action)
random_attack_rule = Rule(get_attacks_condition, get_attacks_action)


# Conjuntos de reglas por tipo de comportamiento
combat_rules = [
    combatant_eat_not_agents_rule,
    combatant_association_proposal_rule,
    combatant_recived_association_proposal_rule,
    combatant_attack_enemy_in_vision,
    combatant_attack_not_enemy_in_vision,
    combatant_move_not_enemy,
    combatant_recived_attacker,
    combatant_default_move,
]

pacifist_rules = [
    pasific_move_away_rule,
    pasific_see_objects_rule,
    pasific_see_actions_rule,
    pasific_default_move,
]

resource_seeker_rules = [
    food_seeker_association_proposal_rule,
    food_seeker_eat_not_enemy_rule,
    food_seeker_eat_enemy_rule,
    food_seeker_stuck_and_resources_available_rule,
    food_seeker_default_move_rule,
]

random_rules = [
    random_association_propose_rule,
    random_recived_association_propose_rule,
    random_move_rule,
    random_attack_rule,
]


def behavior_based_rule_selector(behavior_value, applicable_rules):
    """Retorna una función que actúa como metarregla"""

    def metarule_condition(facts: Set[Fact]):
        behavior = next(
            (fact for fact in facts if fact.key == Knowledge.BEHAVIOR), None
        )
        return behavior and behavior.data == behavior_value

    def metarule_action(facts: Set[Fact]):
        return applicable_rules

    return Rule(metarule_condition, metarule_action, meta_rule=True)


# Crear metarreglas para cada tipo de comportamiento
combat_metarule = behavior_based_rule_selector(1, combat_rules)
pacifist_metarule = behavior_based_rule_selector(2, pacifist_rules)
resource_seeker_metarule = behavior_based_rule_selector(3, resource_seeker_rules)
random_metarule = behavior_based_rule_selector(4, random_rules)
