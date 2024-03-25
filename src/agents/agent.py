import random
from Interfaces.IAgent import IAgent
from Interfaces.IMap import IMapInfoProvider
from agents.interactions import (
    AgentInteractionManager,
    InteractionEvent,
    InteractionType,
)


class Agent(IAgent):
    """
    Representa un agente en la simulación, capaz de moverse, recoger objetos e interactuar con otros agentes.

    Atributos:
        name (str): Nombre del agente.
        health (int): Salud actual del agente.
        x (int): Posición x actual del agente en el mapa.
        y (int): Posición y actual del agente en el mapa.

    """

    def __init__(self, name: str, health: float, x: int, y: int, map: IMapInfoProvider):
        """
        Inicializa una nueva instancia de un agente.

        Parámetros:
            name (str): Nombre del agente.
            health (int): Salud inicial del agente.
            x (int): Posición x inicial del agente.
            y (int): Posición y inicial del agente.
        """
        self.name = name
        self.health = health
        self.map = map
        self.x = x
        self.y = y

    def next_move(self):
        # movimiento aleatorio
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        return dx, dy

    def move(self, dx, dy):
        """
        Mueve el agente en el mapa según los desplazamientos especificados.

        Parámetros:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        self.map.request_move(self, dx, dy)

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def interact(self, other_agent, type=InteractionType.ATTACK):
        """
        Define la lógica de interacción entre este agente y otro. Esto podría incluir combatir, formar alianzas, intercambiar objetos, etc.

        Parámetros:
            other_agent (Agent): El otro agente con el cual este agente interactúa.
        """
        action = random.choice(
            [InteractionType.ATTACK, InteractionType.TRADE, InteractionType.ALLIANCE]
        )
        interaction_event = InteractionEvent(action, self, other_agent)
        AgentInteractionManager().interact(interaction_event)
        # Supongamos que cada agente tiene un 50% de posibilidades de "ganar" el combate
        # if random.choice([True, False]):
        #     print(f"{self.name} ataca a {other_agent.name} y gana.")
        #     other_agent.health -= 10  # El agente atacado pierde salud
        #     # Aquí podrías implementar lógica adicional como verificar si el otro agente ha sido "derrotado"
        # else:
        #     print(f"{self.name} ataca a {other_agent.name} pero pierde.")
        #     self.health -= 10  # El agente atacante pierde salud

    def decide_interaction(self):
        # Verifica las celdas adyacentes para encontrar otros agentes
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:  # Direcciones: arriba, abajo, izquierda, derecha
            x, y = self.x + dx, self.y + dy
            if self.map.valid_position(x, y):
                content = self.map.cell_content(x, y)
                if (
                    isinstance(content, Agent) and content != self
                ):  # Hay otro agente en esta celda
                    if random.choice([True, False]):
                        self.interact(content)
                        return True  # Retorna después de la primera interacción por simplicidad
        return False

    def heuristic(self):
        pass

    def __str__(self) -> str:
        return self.name
