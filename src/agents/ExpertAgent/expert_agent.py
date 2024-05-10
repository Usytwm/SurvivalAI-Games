from math import inf
import os
import sqlite3
from typing import Dict, List, Tuple

import numpy as np
from agents.Agent_with_Memories import Agent_with_Memories
from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import (
    Action,
    Action_Info,
    Action_Type,
    Association_Proposal,
)
from environment.sim_object import Agent_Info, Object_Info, Sim_Object_Type
from agents.ExpertAgent.Rules import (
    combat_metarule,
    pacifist_metarule,
    random_metarule,
    resource_seeker_metarule,
)
from dill import load
from venv import entorno_virtual


def Sensor(aliados, enemigos, recursos, reserva, hostilidades, asociaciones):
    """
    Evalúa las características del entorno y devuelve una tupla con valores que representan la valoración de cada atributo.

    Args:
        aliados (int): Cantidad de aliados presentes en el entorno.
        enemigos (int): Cantidad de enemigos presentes en el entorno.
        recursos (int): Cantidad de recursos visibles en el entorno.
        vitalidad (int): Nivel de vitalidad del agente.
        reserva (int): Cantidad de reservas del agente.
        hostilidades (int): Cantidad de hostilidades ocurridas en el último turno.
        asociaciones (int): Cantidad de asociaciones realizadas en el último turno.

    Returns:
        tuple: Una tupla que representa la valoración de cada atributo en el siguiente orden:
               - Cantidad de aliados valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de enemigos valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de recursos valorada como bajo(1), medio(2) o alto(3).
               - Nivel de vitalidad valorado como bajo(1), medio(2) o alto(3).
               - Cantidad de reservas valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de hostilidades valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de asociaciones valorada como bajo(1), medio(2) o alto(3).
    """
    cantEnemigos = 0
    cantAliados = 0
    cantRecursos = 0
    cantVitalidad = 0
    cantReserva = 0
    cantHostilidades = 0
    cantAsociaciones = 0

    # recursos
    if recursos > 500:
        cantRecursos = 3
    elif 100 < recursos <= 500:
        cantRecursos = 2
    else:
        cantRecursos = 1
    # aliados
    if aliados >= 4:
        cantAliados = 3
    elif 1 < aliados <= 3:
        cantAliados = 2
    else:
        cantAliados = 1
    # enemigos
    if enemigos >= 4:
        cantEnemigos = 3
    elif 1 < enemigos <= 3:
        cantEnemigos = 2
    else:
        cantEnemigos = 1

    # # Vitalidad
    # if vitalidad > 150:
    #     cantVitalidad = 3
    # elif 40 < vitalidad <= 150:
    #     cantVitalidad = 2
    # else:
    #     cantVitalidad = 1
    # Reservas
    if reserva > 150:
        cantReserva = 3
    elif 40 < reserva <= 150:
        cantReserva = 2
    else:
        cantReserva = 1

    # Asociaciones
    if asociaciones > 5:
        cantAsociaciones = 3
    elif 3 <= asociaciones <= 5:
        cantAsociaciones = 3
    else:
        cantAsociaciones = 1

    # Hostilidades
    if hostilidades > 5:
        cantHostilidades = 3
    elif 0 < hostilidades <= 4:
        cantHostilidades = 2
    else:
        cantHostilidades = 1

    return (
        cantAliados,
        cantEnemigos,
        cantRecursos,
        cantReserva,
        cantHostilidades,
        cantAsociaciones,
    )


class ExpertAgent(Agent_with_Memories):
    def __init__(
        self,
        id,
        consume: int,
        reserves,
        conn: sqlite3.Connection,
        trasnsition_function=None,
    ):
        super().__init__(id, consume, reserves, conn)
        self.color = (255, 255, 255)  # white
        if trasnsition_function is None:
            try:
                with open("SuperAgente.joblib", "rb") as a:
                    functions = load(a)
                    self.transition_function = functions[0]
            except:
                self.transition_function = None
        else:
            self.transition_function = trasnsition_function
        initial_facts = [
            Fact(Knowledge.ALLIES, set()),
            Fact(Knowledge.ENEMIES, set()),
            Fact(Knowledge.AGEENTS, set()),
            Fact(Knowledge.NEXT_MOVE, (0, 0)),
            Fact(Knowledge.ID, id),
            Fact(Knowledge.RESERVE, reserves),
            Fact(Knowledge.GEOGRAPHIC_MEMORY, self.geographic_memory),
            Fact(Knowledge.MEMORY_FOR_AGENTS_SIGHTS, self.memory_for_agents_sights),
            Fact(Knowledge.MEMORY_FOR_ATTACKS, self.memory_for_attacks),
            Fact(Knowledge.ASSOCIATION, self.associations),
            Fact(Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, False),
            Fact(Knowledge.BEHAVIOR, 1),
        ]
        initial_rules = [
            combat_metarule,
            pacifist_metarule,
            random_metarule,
            resource_seeker_metarule,
        ]
        self.allies_count = 0
        self.enemies_count = 0
        self.resources_count = 0
        self.vitality = 0
        self.hostility_count = 0
        self.type = 0
        self.estrategy = Estrategy(initial_facts, initial_rules)

    def move(self, possible_moves: List[Tuple[int, int]]):
        # Actualizar los movimientos posibles
        self.estrategy.learn_especific(Knowledge.POSIBLES_MOVEMENTS, possible_moves)
        # Solicitar una decisión de movimiento
        self.type = self.transition()
        self.estrategy.learn_especific(Knowledge.BEHAVIOR, self.type)
        self.estrategy.remove_all_rules()
        decision = self.estrategy.make_decision()
        filter_desicion = list(filter(lambda x: x.key == Knowledge.NEXT_MOVE, decision))
        move = list(
            map(
                lambda x: x.data,
                filter_desicion,
            )
        )[0]
        position = self.estrategy.get_knowledge(Knowledge.POSITION)
        self.estrategy.learn_especific(Knowledge.PREVPOSSITION, position)
        return move

    def inform_move(self, movement: Tuple[int, int]):
        super().inform_move(movement)
        # self.position = position
        # Informar al motor de inferencia la nueva posición
        self.estrategy.learn_especific(Knowledge.POSITION, movement)

    def inform_position(self, position: Tuple[int, int] = None):
        if position:
            self.position = position
            self.estrategy.learn_especific(Knowledge.POSITION, position)

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_received: Tuple[int, int]
    ):
        super().inform_of_attack_received(
            attacker_id, strength, position_attack_received
        )
        # Cuando se recibe un ataque, actualizar los hechos y solicitar una decisión
        self.estrategy.learn_especific(
            Knowledge.RECEIVED_ATTACK,
            (
                attacker_id,
                strength,
                position_attack_received,
            ),
        )
        enemy = self.estrategy.get_knowledge(Knowledge.ENEMIES)
        enemy.add(attacker_id)
        self.estrategy.learn_especific(Knowledge.ENEMIES, enemy)

    def get_attacks(self) -> List[Action]:
        self.type = self.transition()
        self.estrategy.learn_especific(Knowledge.BEHAVIOR, self.type)
        self.estrategy.remove_all_rules()
        decision = self.estrategy.make_decision()
        filtered = list(filter(lambda x: x.key == Knowledge.GETATTACKS, decision))
        if len(filtered) == 0:
            return []
        attacks = list(map(lambda x: x.data, filtered))[0]
        return attacks

    def get_association_proposals(self) -> List:
        self.type = self.transition()
        self.estrategy.learn_especific(Knowledge.BEHAVIOR, self.type)
        self.estrategy.remove_all_rules()
        decision = self.estrategy.make_decision()
        filtered = list(
            filter(lambda x: x.key == Knowledge.GETASSOCIATIONPROPOSALS, decision)
        )
        if len(filtered) == 0:
            return []
        association_Proposal = list(map(lambda x: x.data, filtered))[0]
        return association_Proposal

    def inform_joined_association(
        self,
        association_id: int,
        members: List[int],
        commitments: Dict[int, Tuple[int]],
    ):
        super().inform_joined_association(association_id, members, commitments)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION, self.associations)
        memberss = [m.members for m in self.associations.values()]
        memberss = [item for sublist in memberss for item in sublist]
        allies = set(memberss)
        self.estrategy.learn_especific(Knowledge.ALLIES, allies)

    def inform_broken_association(self, association_id: int):
        super().inform_broken_association(association_id)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION, self.associations)

    def consider_association_proposal(self, proposal: Association_Proposal) -> bool:
        super().consider_association_proposal(proposal)
        self.estrategy.learn_especific(Knowledge.ASSOCIATION_PROPOSALS, proposal)
        desicion = self.estrategy.make_decision()
        filtered = list(
            filter(lambda x: x.key == Knowledge.CONSIDER_ASSOCIATION_PROPOSAL, desicion)
        )
        if len(filtered) == 0:
            return False
        return list(map(lambda x: x.data, filtered))[0]

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        super().inform_of_attack_made(victim_id, strength)

    def take_attack_reward(self, victim_id: int, reward: int):
        super().take_attack_reward(victim_id, reward)
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)

    def see_objects(self, info: List[Object_Info]):
        self.enemies_count = 0
        self.allies_count = 0
        super().see_objects(info)
        # Actualizar la base de hechos con la información de objetos vistos
        self.estrategy.learn_especific(Knowledge.SEE_OBJECTS, info)

        enemy = self.estrategy.get_knowledge(Knowledge.ENEMIES)
        allies = self.estrategy.get_knowledge(Knowledge.ALLIES)

        for i in info:
            if i.type.value == Sim_Object_Type.AGENT.value and isinstance(
                i, Agent_Info
            ):
                if i.id in enemy:
                    self.enemies_count += 1
                if i.id in allies:
                    self.allies_count += 1

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        super().see_resources(info)
        self.estrategy.learn_especific(Knowledge.SEE_RESOURCES, info)

    def see_actions(self, info: List[Action_Info]):
        self.hostility_count = (
            0  #!0 si quieres que en cda turno vea cuantas hostilidades hay
        )
        super().see_actions(info)
        # Actualizar la base de hechos con acciones vistas
        self.estrategy.learn_especific(Knowledge.SEE_ACTIONS, info)
        for i in info:
            if i.type.value == Action_Type.ATTACK.value:
                self.hostility_count += 1

    def feed(self, sugar: int) -> None:
        super().feed(sugar)
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)

    def burn(self) -> None:
        super().burn()
        self.estrategy.learn_especific(Knowledge.RESERVE, self.reserves)

    def cosine_similarity(self, estado1, estado2):
        """
        Calcula la similitud de coseno entre dos estados.

        Args:
            estado1 (tuple): Estado 1 evaluado por la función Sensor.
            estado2 (tuple): Estado 2 evaluado por la función Sensor.

        Returns:
            float: Similitud de coseno entre los dos estados.
        """
        # Convertir tuplas a arrays de numpy
        vector1 = np.array(estado1)
        vector2 = np.array(estado2)

        # Calcular el producto punto entre los dos vectores
        dot_product = np.dot(vector1, vector2)

        # Calcular la magnitud de cada vector
        magnitud1 = np.linalg.norm(vector1)
        magnitud2 = np.linalg.norm(vector2)

        # Calcular la similitud de coseno
        similitud = dot_product / (magnitud1 * magnitud2)

        return similitud

    def transition(
        self,
    ):
        caracteristics = Sensor(
            self.allies_count,
            self.enemies_count,
            self.resources_count,
            self.reserves,
            self.hostility_count,
            len(self.associations),
        )
        transitions = {}

        for function in self.transition_function:
            if function[0][0] == self.type:
                transitions[function[1]] = function

        max_value = -inf
        type_return = self.type
        for key, value in transitions.items():
            current_value = self.cosine_similarity(value[0][1], caracteristics)
            if current_value > max_value:
                max_value = current_value
                type_return = key
        return type_return
