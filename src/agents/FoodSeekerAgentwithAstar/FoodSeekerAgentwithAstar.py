import random
import sqlite3
from typing import Dict, List, Tuple, Set
from Interfaces.IAgent import IAgent
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info, Association_Proposal, Attack
from environment.sim_object import Object_Info
from environment.simple_range import SimpleWalking
from ai.search.pathFinder_with_Astar import PathFinder


class FoodSeekerAgentwithAstar(Agent_with_Memories):
    """Este agente selecciona la casilla que mas azucar tiene de las que conoce, y fija
    trayectoria hacia ella. Sigue la trayectoria fijada mientras ningun otro agente coma el
    azucar que hay en la casilla de destino. Una vez que llega al destino, u otro agente llega
    primero, fija otro objetivo y se mueve hacia el."""

    def __init__(self, id, consume: int, reserves, conn: sqlite3.Connection):
        super().__init__(id, consume, reserves, conn)
        self.color = (255, 0, 255)  # Pink
        self.curse_fixed: List[Tuple[int, int]] = None  # Lista de posiciones a visitar
        self.destination: Tuple[int, int] = None
        self.initial_sugar_in_destination: int = None
        self.path_finder = PathFinder(
            self.geographic_memory.validate_position, self.heuristic, self.cost_function
        )
        self.movement = SimpleWalking()
        self.blocked = False
        self.attacks_planned = []
        self.association_proposals_planned = []

    def distance(self, A: Tuple[int, int], B: Tuple[int, int]) -> int:
        return abs(A[0] - B[0]) + abs(A[1] - B[1])

    def heuristic(self, current: Tuple[int, int], goal: Tuple[int, int]):
        return self.distance(current, goal) / self.initial_sugar_in_destination

    # o sea el costo va a ser mayor que el que tendria si nos movieramos siempre por casillas
    # con tanta azucar como el objetivo, y siempre acercandonos al objetivo

    def cost_function(
        self, A: Tuple[int, int], B: Tuple[int, int], goal: Tuple[int, int]
    ) -> float:
        numerador = 1
        if self.distance(A, goal) <= self.distance(B, goal):
            numerador += 1
            if self.distance(A, goal) < self.distance(B, goal):
                numerador += 1
        # El numerador sera 1 si nos acercamos al objetivo, 2 si nos mantenemos a la misma distancia
        # y 3 si nos alejamos del objetivo
        try:
            f = self.geographic_memory.get_last_info_of_sugar_in_position(B[0], B[1])
            denominador = max(
                self.geographic_memory.get_last_info_of_sugar_in_position(B[0], B[1])[
                    1
                ],
                1,
            )
        except:
            denominador = 1
        return numerador / denominador

    def move(self, possible_moves):
        if self.blocked:
            self.destination = None
            return random.choice(possible_moves)
        if not self.destination:
            self.__find_destination__()
        else:
            actual_sugar_in_destination = (
                self.geographic_memory.get_last_info_of_sugar_in_position(
                    self.destination[0], self.destination[1]
                )[1]
            )
            if actual_sugar_in_destination < self.initial_sugar_in_destination:
                self.__find_destination__()
        move = (
            self.curse_fixed[0][0] - self.position[0],
            self.curse_fixed[0][1] - self.position[1],
        )
        return move

    def __find_destination__(self):
        self.destination, self.initial_sugar_in_destination = (
            self.geographic_memory.get_position_with_most_sugar(
                self.position[0], self.position[1]
            )
        )
        self.curse_fixed = self.path_finder.a_star(
            self.position, self.destination, self.movement.pure_moves()
        )
        self.curse_fixed.pop(0)

    def inform_move(self, movement: Tuple[int, int]):
        self.blocked = movement == (0, 0)
        super().inform_move(movement)
        if self.position == self.curse_fixed[0]:
            self.curse_fixed.pop(0)
    
    def get_association_proposals(self) -> List[Association_Proposal]:
        return self.association_proposals_planned
    
    def get_attacks(self) -> List[Attack]:
        return self.attacks_planned

    def decide_actions_for_next_turn(self) -> None:
        self.attacks_planned, victims = self.decide_attacks_for_next_turn()
        self.association_proposals_planned = self.decide_association_proposals_for_next_turn(victims)

    def decide_attacks_for_next_turn(self) -> Tuple[List[Action], Set[int]]:
        """Ataca a aquellos que pueda destruir de seguro y que amenazan la posicion objetivo"""
        threats = self.memory_for_agents_sights.get_agents_around_position(self.destination)
        threats.sort(key= lambda tpl : tpl[1])
        left_reserves = self.reserves
        attacks = []
        victims = set()
        for other_id, other_resources in threats:
            if other_resources + 1 < left_reserves:
                attacks.append(Attack(self.id, other_id, other_resources + 1))
                victims.add(other_id)
                left_reserves -= (other_resources + 1)
            else:
                break
        return attacks, victims

    def decide_association_proposals_for_next_turn(self, ids_of_victims : Set[int]) -> List:
        """Tratamos de asociarnos a nuestros vecinos agresivos, si no podemos destruirlos direc
        tamente. Siempre las asociaciones son de compromiso 0"""
        answer = []
        for other_id in self.memory_for_agents_sights.agents_seen:
            if other_id in self.memory_for_attacks.deaths or other_id in ids_of_victims:
                continue
            position, _, _ = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
            distance = abs(position[0] - self.position[0]) + abs(position[1] - self.position[1])
            if (distance < 3) and ((self.memory_for_attacks.attacks_per_agent.get(other_id, 0)/self.memory_for_agents_sights.agents_seen[other_id]) > 0.4):
                answer.append(Association_Proposal(self.id, [self.id, other_id], {self.id : (0, 0), other_id : (0, 0)}))
        return answer

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        """No esta dispuesto a ceder ni un quilo. Solo acepta alianzas si un potencial atacante
        esta involucrado y puede de esa manera disuadirlo"""
        if proposal.commitments[self.id][0] > 0:
            return False
        for other_id in proposal.members:
            if not other_id in self.memory_for_agents_sights.agents_seen:
                continue
            position, _, resources = self.memory_for_agents_sights.get_last_info_from_agent(other_id)
            distance = abs(position[0] - self.position[0]) + abs(position[1] - self.position[1])
            if (resources > self.reserves) and (distance < 3) and ((self.memory_for_attacks.attacks_per_agent.get(other_id, 0)/self.memory_for_agents_sights.agents_seen[other_id]) > 0.4):
                return True
        return False
    
    def see_resources(self, info: List[Tuple[Tuple[int] | int]]) -> None:
        super().see_resources(info)
        self.decide_actions_for_next_turn()