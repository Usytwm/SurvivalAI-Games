import sqlite3
from typing import List, Tuple, Dict, Set
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
from environment.actions import Action_Info, Attack, Association_Creation
from environment.sim_object import Object_Info, Agent_Info
from ai.knowledge.knowledge import Knowledge
from environment.actions import Action_Info, Attack
from environment.sim_object import Object_Info
from environment.actions import Action_Type
from environment.association import Association
from agents.memory.memory_for_agents_sights import Memory_for_Agents_Sights
from agents.memory.geographic_memory import Geographic_Memory
from agents.memory.memory_for_attacks import Memory_for_Attacks
from agents.memory.associations_memory import Associations_Memory


class Agent_with_Memories(IAgent):
    def __init__(self, id: int, consume: int, reserves, conn: sqlite3.Connection, movement : IMovement, attack_range : IAttackRange):
        self.id = id
        self.consume = consume
        self.reserves = reserves
        self.position = (0, 0)
        self.iteration = 0
        self.geographic_memory = Geographic_Memory(id)
        self.memory_for_agents_sights = Memory_for_Agents_Sights(id, conn)
        self.memory_for_attacks = Memory_for_Attacks(id, conn)
        self.own_moves: Dict[int, Tuple[int, int]] = {}
        self.positions_visited: Dict[int, Tuple[int, int]] = {}
        self.attacks_made: Dict[int, Tuple[int, int]] = {}
        self.attacks_received: Dict[int, Tuple[int, int]] = {}
        self.memory_for_associations = Associations_Memory(id, conn)
        self.associations: Dict[int, Association] = {}
        self.movement = movement #De esta manera el agente conoce cual es su rango de movimiento y sus movimientos validos
        self.attack_range = attack_range #igualmente con el rango de ataque
        self.allys = set()

    # En IAgent deberiamos cambiar el nombre del parametro position por movement
    def inform_move(self, movement: Tuple[int, int]) -> None:
        self.own_moves[self.iteration] = movement
        self.position = (self.position[0] + movement[0], self.position[1] + movement[1])
        self.positions_visited[self.iteration] = self.position

    def see_objects(self, info: List[Object_Info]) -> None:
        for sight in info:
            if isinstance(sight, Agent_Info):
                other_id = sight.id
                row = sight.position[0] + self.position[0]
                column = sight.position[1] + self.position[1]
                resources = sight.resources
            self.memory_for_agents_sights.add_appearence(
                other_id, row, column, self.iteration, resources
            )
            self.geographic_memory.add_position(row, column)
        self.iteration = self.iteration + 1

    def see_resources(self, info: List[Tuple[Tuple[int] | int]]) -> None:
        for (row, column), sugar in info:
            row = row + self.position[0]
            column = column + self.position[1]
            self.geographic_memory.add_sugar_observation(
                row, column, self.iteration, sugar
            )

    def see_actions(self, info: List[Action_Info]):
        for action in info:
            match action.type.value:
                case Action_Type.DIE.value:
                    self.memory_for_attacks.add_death(action.actor_id, self.iteration)
                case Action_Type.ATTACK.value:
                    self.memory_for_attacks.add_attack(
                        action.actor_id,
                        action.destinataries_ids[0],
                        self.iteration,
                        action.strength,
                    )
                case Action_Type.ASSOCIATION_CREATION.value:
                    self.memory_for_associations.add_association(
                        action.association_id,
                        action.members,
                        action.commitments,
                        self.iteration,
                    )
                case Action_Type.ASSOCIATION_DESTRUCTION.value:
                    # El problema de esto es que no podremos recordar las asociaciones que existieron
                    self.memory_for_associations.remove_association(
                        action.association_id
                    )

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        if not self.iteration in self.attacks_made:
            self.attacks_made[self.iteration] = []
        self.attacks_made[self.iteration].append((victim_id, strength))
        self.reserves -= strength

    def inform_of_attack_received(self, attacker_id: int, strength: int) -> None:
        if not self.iteration in self.attacks_received:
            self.attacks_received[self.iteration] = []
        self.attacks_received[self.iteration].append((attacker_id, strength))
        self.reserves -= strength

    def inform_joined_association(
        self, association_id: int, members: Set[int], commitments: Dict[int, Tuple[int]]
    ):
        association = Association(members, commitments)
        self.associations[association_id] = association
        for member_id in association.members:
            self.allys.add(member_id)

    def inform_broken_association(self, association_id: int):
        self.associations.pop(association_id)

    def burn(self) -> None:
        self.reserves = self.reserves - self.consume

    def feed(self, sugar: int) -> None:
        self.reserves = self.reserves + sugar

    def take_attack_reward(self, victim_id: int, reward: int):
        self.reserves = self.reserves + reward
        self.memory_for_attacks.add_death(victim_id, self.iteration)

    def inform_position(self, position: Tuple[int]) -> None:
        # Por ahora
        pass
