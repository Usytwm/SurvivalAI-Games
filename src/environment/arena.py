import random
import time
from typing import List
from Interfaces.IMap import IMapInfoProvider
from agents.agent import IAgent


class MapController(IMapInfoProvider):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain = [[None for _ in range(width)] for _ in range(height)]
        self.agents: List[IAgent] = []

    def add_agent(self, agent):
        if self.cell_content(agent.x, agent.y) is None:
            self.update_cell(agent.x, agent.y, agent)
            self.agents.append(agent)
        else:
            raise ValueError("Posición ocupada por otro agente.")

    def remove_agent(self, agent):
        self.update_cell(agent.x, agent.y, None)
        self.agents.remove(agent)

    def valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def cell_content(self, x, y):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position")
        return self.terrain[y][x]

    def update_cell(self, x, y, content):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position for object")
        self.terrain[y][x] = content

    def request_move(self, agent, dx, dy):
        new_x = agent.x + dx
        new_y = agent.y + dy
        if (
            self.valid_position(new_x, new_y)
            and self.cell_content(new_x, new_y) is None
        ):
            # Actualizar la celda anterior a None antes de moverse
            self.update_cell(agent.x, agent.y, None)
            # Reflejar el nuevo posicionamiento del agente en el mapa
            self.update_cell(new_x, new_y, agent)
            return True
        return False

    def display(self):
        max_width = 0
        for row in self.terrain:
            for cell in row:
                cell_length = len(str(cell) if cell is not None else "-")
                max_width = max(max_width, cell_length)

        top_bottom_border = "-" + "-" * (
            max_width * len(self.terrain[0]) + len(self.terrain[0])
        )

        print(top_bottom_border)  # Imprime el borde superior.
        for row in self.terrain:
            row_str = "|"
            for cell in row:
                row_str += (str(cell) if cell is not None else "").ljust(
                    max_width
                ) + " "
            print(
                row_str[:-1] + "|"
            )  # Imprimimos la fila y eliminamos el último espacio antes del borde derecho.
        print(top_bottom_border)  # Imprime el borde inferior.


# class GameController:
#     def __init__(self, map_width, map_height, num_agents):
#         self.map = Map(map_width, map_height)
#         self.agents = [
#             Agent(f"Agent {i}", 100, i % map_width, i // map_height)
#             for i in range(num_agents)
#         ]
#         self.update_state()

#     def place_agent_on_map(self, agent):
#         if self.map.valid_position(agent.x, agent.y):
#             self.map.update_cell(agent.x, agent.y, agent)
#         else:
#             raise ValueError("Posición fuera de los límites del mapa.")

#     def move_agent(self, agent, dx, dy):
#         # Asegúrate de limpiar la posición anterior solo si el movimiento es exitoso
#         new_x = agent.x + dx
#         new_y = agent.y + dy
#         if (
#             self.map.valid_position(new_x, new_y)
#             and self.map.cell_content(new_x, new_y) is None
#         ):
#             self.map.update_cell(agent.x, agent.y, None)  # Limpia la celda actual
#             agent.x = new_x
#             agent.y = new_y
#             self.map.update_cell(
#                 new_x, new_y, agent
#             )  # Coloca al agente en la nueva posición
#             return True
#         return False

#     def update_state(self):
#         # Limpia el mapa y luego coloca a cada agente en su posición actual
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 self.map.update_cell(x, y, None)
#         for agent in self.agents:
#             self.place_agent_on_map(agent)

#     def execute_cycle(self):
#         # Ejemplo de movimiento: mueve todos los agentes hacia la derecha
#         for agent in self.agents:
#             self.move_agent(agent, 1, 0)

#     def start(self):
#         while True:
#             self.execute_cycle()
#             self.map.display()
#             time.sleep(1)


# class Map:
#     """
#     Representa el mapa de la simulación, incluyendo el terreno y los objetos colocados en él.

#     Atributos:
#         width (int): Ancho del mapa.
#         height (int): Alto del mapa.
#         terrain (list): Matriz que representa el terreno del mapa.
#         objects (dict): Diccionario de objetos colocados en el mapa, indexados por su posición (x, y).
#     """

#     def __init__(self, width, height):
#         """
#         Inicializa una nueva instancia del mapa con las dimensiones especificadas.

#         Parámetros:
#             width (int): Ancho del mapa.
#             height (int): Alto del mapa.
#         """
#         self.width = width
#         self.height = height
#         self.terrain = [[None for _ in range(width)] for _ in range(height)]
#         # self.objects = {}  # {(x, y): object}

#     def update_cell(self, x, y, content):
#         if not self.valid_position(x, y):
#             raise ValueError("Invalid position for object")
#         self.terrain[y][x] = content

#     def cell_content(self, x, y):
#         if not self.valid_position(x, y):
#             raise ValueError("Invalid position")
#         return self.terrain[y][x]

#     def valid_position(self, x, y):
#         """
#         Verifica si una posición dada está dentro de los límites del mapa.

#         Parámetros:
#             x (int): La posición x a verificar.
#             y (int): La posición y a verificar.

#         Retorna:
#             bool: True si la posición es válida, False en caso contrario.
#         """
#         return 0 <= x < self.width and 0 <= y < self.height

#     def display(self):
#         max_width = 0
#         for row in self.terrain:
#             for cell in row:
#                 cell_length = len(str(cell) if cell else "-")
#                 max_width = max(max_width, cell_length)

#         top_bottom_border = "-" + "-" * (
#             max_width * len(self.terrain[0]) + len(self.terrain[0])
#         )

#         print(top_bottom_border)  # Imprime el borde superior.
#         for row in self.terrain:
#             # Creamos la fila con cada celda ajustada al ancho máximo.
#             row_str = "|"
#             for cell in row:
#                 row_str += (
#                     str(cell).ljust(max_width) + " "
#                 )  # Aseguramos que cada celda tenga el mismo ancho.
#             print(
#                 row_str[:-1] + "|"
#             )  # Imprimimos la fila y eliminamos el último espacio antes del borde derecho.
#         print(top_bottom_border)  # Imprime el borde inferior.


# class Human_Agent(Agent):
#     """
#     Clase que representa un agente humano en la simulación, capaz de tomar decisiones basadas en su entorno y estado.

#     Atributos:
#         name (str): Nombre del agente.
#         health (int): Salud actual del agente.
#         x (int): Posición x actual del agente en el mapa.
#         y (int): Posición y actual del agente en el mapa.
#         inventory (list): Inventario de objetos que el agente ha recogido.
#         state (dict): Diccionario para almacenar estados adicionales del agente (hambre, sed, etc.).
#     """

#     def __init__(self, name, health, x, y):
#         """
#         Inicializa una nueva instancia de un agente humano.

#         Parámetros:
#             name (str): Nombre del agente.
#             health (int): Salud inicial del agente.
#             x (int): Posición x inicial del agente.
#             y (int): Posición y inicial del agente.
#             inventario (list): Lista de objetos que el agente ha recogido.
#             state (dict): Diccionario para almacenar estados adicionales del agente (hambre, sed, etc.).
#         """
#         super().__init__(name, health, x, y)
#         self.inventory = []
#         self.state = {}

#     def decide_actions(self):
#         """
#         Implementar la lógica para que el agente humano tome decisiones basadas en su entorno y estado actual.
#         """
#         # Decision-making logic
#         pass

#     def pick_up_object(self, obj):
#         """
#         Añade un objeto al inventario del agente.

#         Parámetros:
#             obj (Object): El objeto a recoger.
#         """
#         self.inventory.append(obj)


# class Object:
#     """
#     Clase base para objetos que pueden ser colocados en el mapa.

#     Atributos:
#         name (str): Nombre del objeto.
#     """

#     def __init__(self, name):
#         """
#         Inicializa una nueva instancia de un objeto.

#         Parámetros:
#             name (str): El nombre del objeto.
#         """
#         self.name = name


# class Food(Object):
#     """
#     Representa un objeto de comida que puede ser consumido por los agentes.

#     Atributos:
#         nutritional_amount (int): La cantidad de nutrición que proporciona la comida.
#     """

#     def __init__(self, nutritional_amount):
#         """
#         Inicializa una nueva instancia de comida.

#         Parámetros:
#             nutritional_amount (int): La cantidad de nutrición que proporciona la comida.
#         """
#         super().__init__("Food")
#         self.nutritional_amount = nutritional_amount


# class Weapon(Object):
#     """
#     Representa un arma que puede ser utilizada por los agentes para luchar.

#     Atributos:
#         damage (int): El daño que el arma puede infligir.
#     """

#     def __init__(self, damage):
#         """
#         Inicializa una nueva instancia de un arma.

#         Parámetros:
#             damage (int): El daño que el arma puede infligir.
#         """
#         super().__init__("Weapon")
#         self.damage = damage
