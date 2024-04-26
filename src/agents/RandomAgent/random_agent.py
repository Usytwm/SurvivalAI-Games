from typing import List, Tuple
from environment.sim_object import Object_Info
from environment.actions import Action_Info, Action
from Interfaces.IAgent import IAgent
from random import randint, random

from typing import List, Tuple

from ai.knowledge.knowledge import Estrategy, Fact, Knowledge
from environment.actions import Action, Action_Info
from environment.sim_object import Object_Info
from Interfaces.IAgent import IAgent
from agents.RandomAgent.Rules import move_rule, attack_rule


class RandomAgent(IAgent):
    def __init__(self, id):
        self.id = id
        self.color = (255, 255, 0)  # yellowF
        initial_facts = [
            Fact(Knowledge.ALLIES, set()),
            Fact(Knowledge.ENEMIES, set()),
            Fact(Knowledge.AGEENTS, set()),
            Fact(Knowledge.NEXT_MOVE, (0, 0)),
            Fact(Knowledge.ID, id),
        ]
        initial_rules = [move_rule, attack_rule]

        self.estrategy = Estrategy(initial_facts, initial_rules)

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

    def inform_move(self, position: Tuple[int, int]):
        self.position = position
        self.estrategy.learn_especific(Knowledge.POSITION, position)

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

    def inform_move(self, position: Tuple[int, int]):
        self.position = position
        self.estrategy.learn_especific(Knowledge.POSITION, position)

    def get_attacks(self) -> List[Action]:
        decision = self.estrategy.make_decision()
        filtered = list(filter(lambda x: x.key == Knowledge.GETATTACKS, decision))
        if len(filtered) == 0:
            return []
        attacks = list(map(lambda x: x.data, filtered))[0]
        return attacks

    def get_association_proposals(self) -> List:
        return []  # Todo implementar

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        #! pendiente
        pass

    def take_attack_reward(self, victim_id: int, reward: int):
        #! pendiente
        pass

    def see_objects(self, info: List[Object_Info]):
        self.estrategy.learn_especific(Knowledge.SEE_OBJECTS, info)

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        self.estrategy.learn_especific(Knowledge.SEE_RESOURCES, info)

    def see_actions(self, info: List[Action_Info]):
        self.estrategy.learn_especific(Knowledge.SEE_ACTIONS, info)

    def feed(self, sugar: int) -> None:
        self.estrategy.learn_especific(Knowledge.FEED, sugar)

    def burn(self) -> None:
        self.estrategy.learn_especific(Knowledge.BURN, True)


# class Random_Agent(IAgent):
#     def __init__(self, id):
#         self.id = id

#     def move(self) -> Tuple[int, int]:
#         directions = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
#         return directions[randint(0, 4)]

#     def inform_move(self, position: Tuple[int]) -> None:
#         pass

#     def get_attacks(self) -> List[Action]:
#         attacks = []
#         for i in range(1, 5):
#             if random() < 0.5:
#                 attacks.append(Attack(self.id, i, 1))
#         return attacks

#     def get_association_proposals(self) -> List:
#         return []

#     def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
#         print(
#             f"{self.id} ha realizado un ataque a "
#             + str(victim_id)
#             + " con fuerza "
#             + str(strength)
#         )

#     def inform_of_received_attack(self, attacker_id: int, strength: int) -> None:
#         print(
#             f"{self.id} ha recibido un ataque de "
#             + str(attacker_id)
#             + " con fuerza "
#             + str(strength)
#         )

#     def take_attack_reward(self, victim_id: int, reward: int):
#         print(
#             "He cobrado una recompensa de "
#             + str(reward)
#             + " por matar a "
#             + str(victim_id)
#         )

#     def see_objects(self, info: List[Object_Info]) -> None:
#         for obj in info:
#             print(str(obj.position) + " : " + str(obj.id))
#         pass

#     def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
#         pass

#     def see_actions(self, info: List[Action_Info]):
#         for action in info:
#             print(str(action.type) + " in " + str(action.start_position))

#         print("End of actions")

#     def feed(self, sugar: int) -> None:
#         pass

#     def burn(self) -> None:
#         pass
