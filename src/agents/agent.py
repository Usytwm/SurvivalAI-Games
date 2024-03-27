import random
from typing import Dict, NamedTuple, Tuple
from Interfaces.IAgent import IAgent
from Interfaces.IMap import IMapInfoProvider
from agents.interactions import (
    AgentInteractionManager,
    InteractionEvent,
    InteractionType,
)
from environment.arena import MapController


class AgentInfo(NamedTuple):
    health: float
    strength: float
    position: Tuple[int, int]
    is_ally: bool


class Agent(IAgent):
    def __init__(
        self,
        name: str,
        health: float,
        strength: float,
        vision_range: int,
        x: int,
        y: int,
        map: MapController,
    ):
        self.name = name
        self.health = health
        self.strength = strength
        self.x = x
        self.y = y
        self.vision_range = vision_range
        self.map = map
        self.internal_map = MapController(self.map.width, self.map.height)
        self.allies = set()  # Nombres de los agentes aliados.
        self.known_agents: Dict[str, AgentInfo] = (
            {}
        )  # conocimiento sobre klos agentes que ha visto
        self.inventory = {}  # Inventario del agente
        self.update_vision()

        # Suponiendo que IAgent es la interfaz base para Agent.

    def attack(self, target: IAgent):
        if target.name not in self.allies:
            # Lógica para calcular el daño basado en la fuerza y otros atributos.
            damage = self.strength  # Daño básico
            target.interact(self, InteractionType.DEFEND, data=damage)

    def defend(self, damage, attacker: IAgent):
        # Ejemplo simple: reducir el daño basado en algún atributo de defensa
        self.health -= max(
            damage, 0
        )  # Asegurar que la salud no aumente debido a la defensa
        print(f"{attacker.name} ataca a {self.name} y le inflige {damage} de daño.")
        if self.health <= 0:
            print(f"{self.name} ha sido derrotado.")
            self.map.remove_agent(self)
        if self.name in self.allies:
            self.remove_ally(attacker.name)

    def decide_next_move(self):
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        return dx, dy

    def move(self, dx, dy):
        request_move = self.map.request_move(self, dx, dy)
        if request_move:
            self.update_position(self.x + dx, self.y + dy)
        self.update_vision()

    def add_ally(self, agent_name):
        print(f"{self.name} forma una alianza con {agent_name}")
        self.allies.add(agent_name)
        self.known_agents[agent_name].is_ally = True

    def remove_ally(self, agent_name):
        """Remueve un agente de la lista de aliados."""
        if agent_name in self.allies:
            self.allies.remove(agent_name)

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.update_vision()

    def update_vision(self):
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                x, y = self.x + dx, self.y + dy
                if self.map.valid_position(x, y):
                    content = self.map.cell_content(x, y)
                    self.internal_map.update_cell(x, y, content)
                    if isinstance(content, Agent) and content.name != self.name:
                        # Actualiza la memoria del agente con la información del agente visto.
                        self.known_agents[content.name] = AgentInfo(
                            health=content.health,
                            strength=content.strength,
                            position=(content.x, content.y),
                            is_ally=content.name in self.allies,
                        )

    def interact(self, other_agent, type=InteractionType.ATTACK, data=None):
        interaction_event = InteractionEvent(
            type, self, other_agent, map=self.map, data=data
        )
        AgentInteractionManager().interact(interaction_event)

    def decide_interaction(self):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = self.x + dx, self.y + dy
            if self.map.valid_position(x, y):
                content = self.map.cell_content(x, y)
                action = random.choice(
                    [
                        InteractionType.ATTACK,
                        InteractionType.TRADE,
                        InteractionType.ALLIANCE,
                    ]
                )
                if isinstance(content, Agent) and content != self:
                    if random.choice(
                        [True, False]
                    ):  # 50% para decidir si interactuar o no
                        self.interact(
                            content,
                            action,
                        )
                        return True
        return False

    def heuristic(self):
        pass

    def __str__(self) -> str:
        return self.name


# class Agent(IAgent):
#     """
#     Representa un agente en la simulación, capaz de moverse, recoger objetos e interactuar con otros agentes.

#     Atributos:
#         name (str): Nombre del agente.
#         health (int): Salud actual del agente.
#         x (int): Posición x actual del agente en el mapa.
#         y (int): Posición y actual del agente en el mapa.

#     """

#     def __init__(self, name: str, health: float, x: int, y: int, map: IMapInfoProvider):
#         """
#         Inicializa una nueva instancia de un agente.

#         Parámetros:
#             name (str): Nombre del agente.
#             health (int): Salud inicial del agente.
#             x (int): Posición x inicial del agente.
#             y (int): Posición y inicial del agente.
#         """
#         self.name = name
#         self.health = health
#         self.map = map
#         self.x = x
#         self.y = y

#     def next_move(self):
#         # movimiento aleatorio
#         dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
#         return dx, dy

#     def move(self, dx, dy):
#         """
#         Mueve el agente en el mapa según los desplazamientos especificados.

#         Parámetros:
#             dx (int): Desplazamiento en el eje x.
#             dy (int): Desplazamiento en el eje y.
#         """
#         self.map.request_move(self, dx, dy)

#     def update_position(self, new_x, new_y):
#         self.x = new_x
#         self.y = new_y

#     def interact(self, other_agent, type=InteractionType.ATTACK):
#         """
#         Define la lógica de interacción entre este agente y otro. Esto podría incluir combatir, formar alianzas, intercambiar objetos, etc.

#         Parámetros:
#             other_agent (Agent): El otro agente con el cual este agente interactúa.
#         """
#         action = random.choice(
#             [InteractionType.ATTACK, InteractionType.TRADE, InteractionType.ALLIANCE]
#         )
#         interaction_event = InteractionEvent(action, self, other_agent)
#         AgentInteractionManager().interact(interaction_event)
#         # Supongamos que cada agente tiene un 50% de posibilidades de "ganar" el combate
#         # if random.choice([True, False]):
#         #     print(f"{self.name} ataca a {other_agent.name} y gana.")
#         #     other_agent.health -= 10  # El agente atacado pierde salud
#         #     # Aquí podrías implementar lógica adicional como verificar si el otro agente ha sido "derrotado"
#         # else:
#         #     print(f"{self.name} ataca a {other_agent.name} pero pierde.")
#         #     self.health -= 10  # El agente atacante pierde salud

#     def decide_interaction(self):
#         # Verifica las celdas adyacentes para encontrar otros agentes
#         for dx, dy in [
#             (-1, 0),
#             (1, 0),
#             (0, -1),
#             (0, 1),
#         ]:  # Direcciones: arriba, abajo, izquierda, derecha
#             x, y = self.x + dx, self.y + dy
#             if self.map.valid_position(x, y):
#                 content = self.map.cell_content(x, y)
#                 if (
#                     isinstance(content, Agent) and content != self
#                 ):  # Hay otro agente en esta celda
#                     if random.choice([True, False]):
#                         self.interact(content)
#                         return True  # Retorna después de la primera interacción por simplicidad
#         return False

#     def heuristic(self):
#         pass

#     def __str__(self) -> str:
#         return self.name
