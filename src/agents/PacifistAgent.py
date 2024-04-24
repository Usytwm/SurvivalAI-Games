import math
from random import random
from typing import Any, Dict, List, Tuple
from Interfaces.IAgent import IAgent
from ai.knowledge.knowledge import BaseKnowledge, Estrategy, Knowledge
from environment.actions import Action, Action_Info, Action_Type, Attack
from environment.sim_object import Object_Info, Sim_Object_Type


def move_away_from_attacker(current_pos, attacker_pos, possible_moves):
    # Desempaquetar las posiciones actuales
    x1, y1 = current_pos
    x2, y2 = attacker_pos

    # Inicializar la mejor posición y la mayor distancia encontrada
    best_move = None
    max_distance = -float("inf")

    # Evaluar cada movimiento posible
    for move in possible_moves:
        # Calcular la nueva posición si se toma este movimiento
        new_x, new_y = x1 + move[0], y1 + move[1]

        # Calcular la distancia desde la nueva posición al atacante
        distance = math.sqrt((x2 - new_x) ** 2 + (y2 - new_y) ** 2)

        # Si la distancia es mayor que la máxima encontrada, actualizar
        if distance > max_distance:
            max_distance = distance
            best_move = (move[0], move[1])

    return best_move


class PacifistEstrategy(Estrategy):
    def __init__(self, knowledge_base: Dict[Knowledge, Any] = None):
        super().__init__(knowledge_base)
        self.view_agents = {}
        self.view_agent_attacks = {}

    def learn(self, data: Dict[Knowledge, Any]):
        for key in data.keys():
            self.knowledge_base[key] = data[key]

    def learn_especific(self, key: Knowledge, data: Any):
        self.knowledge_base[key] = data

    def make_decision(self):
        recived_attack_info = self.get_knowledge(Knowledge.RECEIVED_ATTACK)
        allies_info = self.get_knowledge(Knowledge.ALLIES)
        enemies_info = self.get_knowledge(Knowledge.ENEMIES)
        current_pos = self.get_knowledge(Knowledge.POSITION)
        possible_moves = self.get_knowledge(Knowledge.POSIBLES_MOVEMENTS)
        if recived_attack_info:
            attacker_id, _, position_attack_recived = recived_attack_info
            try:
                self.view_agents[attacker_id] += 1
            except KeyError:
                self.view_agents[attacker_id] = 1
            try:
                self.view_agent_attacks[attacker_id] += 1
            except KeyError:
                self.view_agent_attacks[attacker_id] = 1
            if allies_info:
                if attacker_id in allies_info:
                    allies_info.remove(attacker_id)
                enemies_info.add(attacker_id)
            best_move = move_away_from_attacker(
                current_pos, position_attack_recived, possible_moves
            )
            return best_move

        see_objects_info = self.get_knowledge(Knowledge.SEE_OBJECTS)
        if see_objects_info:
            for obj in see_objects_info:
                if obj.type.value == Sim_Object_Type.AGENT.value:
                    try:
                        self.view_agents[obj.id] += 1
                    except KeyError:
                        self.view_agents[obj.id] = 1
                    if obj.id in enemies_info:
                        x_1, y_1 = current_pos
                        x_2, y_2 = obj.position
                        possible_moves = self.get_knowledge(
                            Knowledge.POSIBLES_MOVEMENTS
                        )
                        best_move = move_away_from_attacker(
                            current_pos, (x_1 + x_2, y_1 + y_2), possible_moves
                        )
                        return best_move

        see_actions_info = self.get_knowledge(Knowledge.SEE_ACTIONS)
        if see_actions_info:
            for action in see_actions_info:
                if action.type == Action_Type.ATTACK:
                    id = action.agent_id
                    try:
                        self.view_agent_attacks[id] += 1
                    except KeyError:
                        self.view_agent_attacks[id] = 1
                    if id in enemies_info:
                        x_1, y_1 = current_pos
                        x_2, y_2 = action.position
                        possible_moves = self.get_knowledge(
                            Knowledge.POSIBLES_MOVEMENTS
                        )
                        best_move = move_away_from_attacker(
                            current_pos, (x_1 + x_2, y_1 + y_2), possible_moves
                        )
                        return best_move

        # TODO Akie s donde vendria la busqueda para encontrar la mejor posicion a la que moverme teniendo en cuenat que no tengo ningun atacante o enemigo cerca, una busqueda peobabilistica
        # TODO que probabilidad de uqe si no es mi enemigo hay de qued me ataque,
        # TODO necesito tener una cuenta de las acciones que ha hecho ese agente
        # TODO cuando lo he visto, eso puede ir dspues de este if
        # TODO TENGO que ver aki xq pueden haber varios agentes aue seane nemigis mios ,
        # TODO tengo que elegir a cual posicion me hace menos dano, aki se puede incluir el problema de busqueda, teenr una funcionde evaluacionde cuanto dano me puede hacer cada agente y quedarme con al mejor solucion y moverme ahi
        return super().make_decision()

    def get_knowledge(self, key: Knowledge):
        try:
            return self.knowledge_base[key]
        except KeyError:
            return None


class PacifistAgent(IAgent):
    def __init__(self, id):
        self.id = id
        dict_knowledge = {
            Knowledge.ALLIES: set(),
            Knowledge.ENEMIES: set(),
            Knowledge.AGEENTS: set(),
            Knowledge.POSIBLES_MOVEMENTS: [(0, 0)],
        }
        self.estrategy = PacifistEstrategy(dict_knowledge)

    def move(self, possible_moves) -> Tuple[int, int]:
        self.estrategy.learn_especific(Knowledge.POSIBLES_MOVEMENTS, possible_moves)
        """Decide el siguiente movimiento basado en el recurso más cercano y rico en azúcar."""
        x = self.estrategy.make_decision()
        return x

    def inform_move(self, position: Tuple[int, int]):
        self.position = position
        self.estrategy.learn_especific(Knowledge.POSITION, position)
        # print(f"Se ha movido a la posición {position}")

    def inform_position(
        self, position: Tuple[int] = None, reserve: int = None, health: int = None
    ) -> None:
        if position:
            self.position = position
            self.estrategy.learn_especific(Knowledge.POSITION, position)
        if reserve:
            self.reserve = reserve
            self.estrategy.learn_especific(Knowledge.RESERVE, reserve)
        if health:
            self.health = health
            self.estrategy.learn_especific(Knowledge.HEALTH, health)

    def get_attacks(self) -> List[Action]:
        # * No ataca, solo tiene aliados
        return []
        # if randint(0, 100) < 20:  # 20% chance to attack
        #     target_id = randint(1, 10)  # Random target for example
        #     return [Attack(self.id, target_id, 1)]
        # return []

    def get_association_proposals(self) -> List:
        return []  # Todo implementar

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        # * Aki no dbe hacer nada ya que no ataca, solo busca escapar de los ataques y de los que no son sus aliados
        # print(f"Attack made on agent {victim_id} with strength {strength}")
        pass

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_recived: Tuple[int, int]
    ) -> None:
        self.estrategy.learn_especific(
            Knowledge.RECEIVED_ATTACK, (attacker_id, strength, position_attack_recived)
        )
        # print(f"Received attack from agent {attacker_id} with strength {strength}")

    def take_attack_reward(self, victim_id: int, reward: int):
        # print(f"Received reward of {reward} for defeating agent {victim_id}")
        pass

    def see_objects(self, info: List[Object_Info]) -> None:
        # self.current_see_objects = info
        self.estrategy.learn_especific(Knowledge.SEE_OBJECTS, info)
        # print(f"Seeing objects: {info}")

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        # self.current_see_resources = info
        self.estrategy.learn_especific(Knowledge.SEE_RESOURCES, info)
        # print(f"Seeing resources: {info}")

    def see_actions(self, info: List[Action_Info]):
        # self.current_see_actions = info
        self.estrategy.learn_especific(Knowledge.SEE_ACTIONS, info)
        # print(f"Actions seen: {info}")

    def feed(self, sugar: int) -> None:
        self.estrategy.learn_especific(Knowledge.FEED, sugar)
        # print(f"Received {sugar} units of sugar")

    def burn(self) -> None:
        self.estrategy.learn_especific(Knowledge.BURN, True)
        # print("Consuming daily ration of sugar")
