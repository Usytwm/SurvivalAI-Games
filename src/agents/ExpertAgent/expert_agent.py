from typing import List, Tuple
from experta import *
from random import shuffle, random
from Interfaces.IAgent import IAgent

from environment.sim_object import Object_Info, Sim_Object
from environment.actions import Action_Info, Attack, Action


class EstadoAgente(Fact):
    """Información sobre el estado del agente en el juego."""

    salud = Field(int, default=100)
    posicion = Field(tuple, default=(0, 0))
    amenaza_cercana = Field(bool, default=False)
    recurso_cercano = Field(tuple, default=None)
    objetivo = Field(str, default="explorar")
    # TODO accion paara saber que se sta haciendo o que se va a hacer
    # TODO movimineto para saber que se puede hacer
    # mov = Field(tuple, default=None)


class SistemaDecisionAgente(KnowledgeEngine):
    # @DefFacts()
    # def setup_initial_conditions(self):
    #     yield EstadoAgente(salud=100, posicion=(0, 0), objetivo="explorar")

    @Rule(EstadoAgente(recurso_cercano=MATCH.recurso & P(lambda x: x is not None)))
    def ir_a_recurso(self, recurso):
        print(f"Recurso detectado en {recurso}, moviéndose hacia el recurso.")
        self.declare(EstadoAgente(objetivo="recolectar", recurso_cercano=recurso))

    @Rule(EstadoAgente(salud=P(lambda x: x < 50), amenaza_cercana=False))
    def buscar_curacion(self):
        print("Salud baja, buscando curación.")
        self.declare(EstadoAgente(objetivo="buscar_curacion"))

    @Rule(EstadoAgente(objetivo="huir"))
    def huir(self):
        print("Huyendo de la amenaza.")
        self.declare(EstadoAgente(objetivo="explorar"))

    @Rule(EstadoAgente(amenaza_cercana=True))
    def huir_de_amenaza(self):
        print("Amenaza detectada cerca, huyendo.")
        self.declare(EstadoAgente(objetivo="huir"))

    @Rule(EstadoAgente(recurso_cercano=MATCH.recurso & P(lambda x: x is not None)))
    def ir_a_recurso(self, recurso):
        print(f"Recurso detectado en {recurso}, moviéndose hacia el recurso.")
        self.declare(EstadoAgente(objetivo="recolectar"))

    @Rule(EstadoAgente(objetivo="recolectar"))
    def recolectar_recurso(self):
        print("Recolectando recurso.")
        self.declare(EstadoAgente(objetivo="explorar"))


class ExpertAgent(IAgent, KnowledgeEngine):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.position = (0, 0)
        self.current_see_objects = []
        self.current_see_resources = []
        self.current_see_actions = []
        self.reserve = 0
        self.health = 100
        self.threat_nearby = False
        self.resource_nearby = None
        self.attack_received = False
        self.attack_strength = 0
        self.next_move = (0, 0)
        self.expert_system = self
        self.expert_system.reset()

    # todo tengo que poner dentro de los rule los metodos que se ejecutararn caundo se cumpla cada regla y se vea reflejado en el agnete

    @Rule(EstadoAgente(salud=P(lambda x: x < 50), amenaza_cercana=False))
    def buscar_curacion(self):
        print("Salud baja, buscando curación.")
        self.declare(EstadoAgente(objetivo="buscar_curacion"))

    @Rule(EstadoAgente(objetivo="huir"))
    def huir(self):
        print("Huyendo de la amenaza.")
        self.declare(EstadoAgente(objetivo="explorar"))

    @Rule(EstadoAgente(amenaza_cercana=True))
    def huir_de_amenaza(self):
        print("Amenaza detectada cerca, huyendo.")
        self.declare(EstadoAgente(objetivo="huir"))

    @Rule(EstadoAgente(recurso_cercano=MATCH.recurso & P(lambda x: x is not None)))
    def ir_a_recurso(self, recurso):
        print(f"Recurso detectado en {recurso}, moviéndose hacia el recurso.")
        self.declare(EstadoAgente(objetivo="recolectar"))

    @Rule(EstadoAgente(objetivo="recolectar"))
    def recolectar_recurso(self):
        print("Recolectando recurso.")
        self.declare(EstadoAgente(objetivo="explorar"))

    def update_expert_system(self, possible_moves: List[Tuple[int, int]]):
        possible_moves.remove((0, 0))
        """Actualiza y procesa el sistema experto con los datos actuales del agente."""
        valid_resource_positions = filter(
            lambda pos: pos[0] in possible_moves,
            [res_pos for res_pos in self.current_see_resources],
        )
        # Convertir las posiciones filtradas en una lista
        valid_resource_positions = list(valid_resource_positions)
        shuffle(valid_resource_positions)

        best_resource = max(valid_resource_positions, key=lambda x: x[1], default=None)
        self.expert_system.reset()
        self.expert_system.declare(
            EstadoAgente(
                posicion=self.position,
                recurso_cercano=best_resource[0] if best_resource else None,
            )
        )
        self.expert_system.run()

    def move(self, possible_moves) -> Tuple[int, int]:
        """Decide el siguiente movimiento basado en el recurso más cercano y rico en azúcar."""
        self.update_expert_system(possible_moves)
        for fact_id, fact in self.expert_system.facts.items():
            if isinstance(fact, EstadoAgente):
                resource_pos = fact.get("recurso_cercano", None)
                if resource_pos:
                    print(
                        f"Agnte {self.id} Decidido mover hacia el recurso en {resource_pos}."
                    )
                    return resource_pos
        # if resource_pos:
        #     print(f"Decidido mover hacia el recurso en {resource_pos}.")
        #     return resource_pos
        return (0, 0)

    def inform_move(self, movement: Tuple[int, int]):
        self.position = movement
        print(f"Se ha movido a la posición {movement}")

    def inform_position(
        self, position: Tuple[int] = None, reserve: int = None, health: int = None
    ) -> None:
        if position:
            self.position = position
        if reserve:
            self.reserve = reserve
        if health:
            self.health = health

    def get_attacks(self) -> List[Action]:
        attacks = []
        for i in range(1, 2):
            if random() < 0.5:
                attacks.append(Attack(self.id, i, 1))
        return attacks
        # if randint(0, 100) < 20:  # 20% chance to attack
        #     target_id = randint(1, 10)  # Random target for example
        #     return [Attack(self.id, target_id, 1)]
        # return []

    def get_association_proposals(self) -> List:
        return []

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        print(f"Attack made on agent {victim_id} with strength {strength}")

    def inform_of_received_attack(self, attacker_id: int, strength: int) -> None:
        print(f"Received attack from agent {attacker_id} with strength {strength}")

    def take_attack_reward(self, victim_id: int, reward: int):
        print(f"Received reward of {reward} for defeating agent {victim_id}")

    def see_objects(self, info: List[Object_Info]) -> None:
        self.current_see_objects = info
        print(f"Seeing objects: {info}")

    def see_resources(self, info: List[Tuple[Tuple[int, int], int]]) -> None:
        self.current_see_resources = info
        print(f"Seeing resources: {info}")

    def see_actions(self, info: List[Action_Info]):
        self.current_see_actions = info
        print(f"Actions seen: {info}")

    def feed(self, sugar: int) -> None:
        print(f"Received {sugar} units of sugar")

    def burn(self) -> None:
        print("Consuming daily ration of sugar")
