from typing import List, Tuple
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action, Attack
from Interfaces.IAgent import IAgent
from random import randint

from typing import Tuple, List
from environment.actions import Action, MoveAction, AttackAction
from environment.sim_object import Object_Info


class MyAgent(IAgent):
    def __init__(self):
        
        self.my_id = None  # Se guardará el id del agente cuando se conozca
        self.last_position = None  # Ultima posición conocida del agente
        self.enemy_ids = []  # Lista de ids de enemigos conocidos

    def move(self, possible_movements: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Elige un movimiento en función de la posición de los recursos y enemigos
        """

        # Prioridad 1: Recolectar recursos
        best_move = None
        best_resource_percentage = 0
        for move in possible_movements:
            new_position = (self.last_position[0] + move[0], self.last_position[1] + move[1])
            if self.map.IsValid(new_position):
                resource_percentage = self.map.resource_percentage(new_position)
                if resource_percentage > best_resource_percentage:
                    best_move = new_position
                    best_resource_percentage = resource_percentage

        # Prioridad 2: Alejarse de enemigos (si se conocen)
        if best_move is None and self.enemy_ids:
            for move in possible_movements:
                new_position = (self.last_position[0] + move[0], self.last_position[1] + move[1])
                if self.map.IsValid(new_position):
                    # Evitar posiciones adyacentes a enemigos
                    is_safe = True
                    for enemy_id in self.enemy_ids:
                        enemy_position = self.map.peek_id(enemy_id)
                        if abs(enemy_position[0] - new_position[0]) <= 1 and abs(enemy_position[1] - new_position[1]) <= 1:
                            is_safe = False
                            break
                    if is_safe:
                        return new_position

        # Regresa el mejor movimiento encontrado o uno aleatorio si no hay ninguno
        return best_move if best_move is not None else possible_movements[0]

    def get_actions(self, possible_victims: List[int]) -> List[Action]:
        """Ataca a enemigos cercanos si es posible"""
        actions = []
        for enemy_id in possible_victims:
            enemy_position = self.map.peek_id(enemy_id)
            if enemy_position is not None and self.last_position is not None:
                # Solo atacar a enemigos adyacentes
                if abs(enemy_position[0] - self.last_position[0]) <= 1 and abs(enemy_position[1] - self.last_position[1]) <= 1:
                    actions.append(AttackAction(enemy_id))
                    self.enemy_ids.append(enemy_id)  # Marcar como enemigo
        return actions

    def inform_move(self, position: Tuple[int, int]) -> None:
        self.last_position = position

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        # Actualizar lista de enemigos si la víctima es eliminada
        if victim_id in self.enemy_ids:
            self.enemy_ids.remove(victim_id)

    def inform_of_attack_received(self, attacker_id: int, strength: int) -> None:
        # Agregar atacante a lista de enemigos si no estaba
        if attacker_id not in self.enemy_ids:
            self.enemy_ids.append(attacker_id)

    def see_objects(self, info: List[Object_Info]) -> None:
        # Identificar el propio agente para futuras referencias
        for obj in info:
            if obj.id is not None and obj.name == "MyAgent":
                self.my_id = obj.id
                break

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        # No usado por esta implementación básica
