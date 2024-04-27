from typing import List, Tuple

from ai.knowledge.knowledge import Knowledge
from environment.actions import Action, Action_Info
from environment.sim_object import Object_Info
from Interfaces.IAgent import IAgent
from agents.PacifistAgent.strategy import PacifistEstrategy


class PacifistAgent(IAgent):
    def __init__(self, id):
        self.id = id
        self.estrategy = PacifistEstrategy()

    def move(self, possible_moves: List[Tuple[int, int]]):
        # Actualizar los movimientos posibles
        self.estrategy.learn_especific(Knowledge.POSIBLES_MOVEMENTS, possible_moves)
        # Solicitar una decisión de movimiento
        decision = self.estrategy.make_decision()
        move = list(
            map(
                lambda x: x.data,
                list(filter(lambda x: x.key == Knowledge.NEXT_MOVE, decision)),
            )
        )[0]
        return move

    def inform_move(self, movement: Tuple[int, int]):
        self.position = movement
        # Informar al motor de inferencia la nueva posición
        self.estrategy.learn_especific(Knowledge.POSITION, movement)

    def inform_position(
        self, position: Tuple[int, int] = None, reserve: int = None, health: int = None
    ):
        if position:
            self.position = position
            self.estrategy.learn_especific(Knowledge.POSITION, position)
        if reserve:
            self.reserve = reserve
            self.estrategy.learn_especific(Knowledge.RESERVE, reserve)
        if health:
            self.health = health
            self.estrategy.learn_especific(Knowledge.HEALTH, health)

    def inform_of_attack_received(
        self, attacker_id: int, strength: int, position_attack_received: Tuple[int, int]
    ):
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
        # decision = self.estrategy.make_decision()
        # return decision

    def inform_move(self, movement: Tuple[int, int]):
        self.position = movement
        self.estrategy.learn_especific(Knowledge.POSITION, movement)

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

    def take_attack_reward(self, victim_id: int, reward: int):
        # print(f"Received reward of {reward} for defeating agent {victim_id}")
        pass

    def see_objects(self, info: List[Object_Info]):
        # Actualizar la base de hechos con la información de objetos vistos
        self.estrategy.learn_especific(Knowledge.SEE_OBJECTS, info)

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        # self.current_see_resources = info
        self.estrategy.learn_especific(Knowledge.SEE_RESOURCES, info)
        # print(f"Seeing resources: {info}")

    def see_actions(self, info: List[Action_Info]):
        # Actualizar la base de hechos con acciones vistas
        self.estrategy.learn_especific(Knowledge.SEE_ACTIONS, info)

    def feed(self, sugar: int) -> None:
        self.estrategy.learn_especific(Knowledge.FEED, sugar)
        # print(f"Received {sugar} units of sugar")

    def burn(self) -> None:
        self.estrategy.learn_especific(Knowledge.BURN, True)
        # print("Consuming daily ration of sugar")
