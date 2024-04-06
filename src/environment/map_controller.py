import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/enviroment')
sys.path.insert(0, current_dir + '/src/ai')
sys.path.insert(0, current_dir + '/src/interfaces')
from typing import List, Dict, Tuple
from environment.objects import Object_Type
from Interfaces.IMap import IMapInfoProvider
import math
class Map(IMapInfoProvider):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain = [[None for _ in range(width)] for _ in range(height)]
        self.object_positions : Dict[str, Tuple[int, int]] = {}
        self.agent_positions : Dict[str, Tuple[int, int]] = {}

    def add_object(self, x, y, id : str, is_agent = False):
        if self.cell_content(x, y) is None:
            self.update_cell(x, y, id, is_agent)
        else:
            raise ValueError("Posición ocupada.")

    def remove_object(self, x, y, is_agent = False):
        self.update_cell(x, y, None)

    def valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def cell_content(self, x, y):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position")
        return self.terrain[y][x]

    def update_cell(self, x, y, content, is_agent = False):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position for object")
        self.object_positions[content] = (x, y)
        if is_agent:
            self.agent_positions[content] = (x, y)
        self.terrain[y][x] = content

    def move(self, sx, sy, dx, dy):
        if (
            self.valid_position(dx, dy)
            and self.cell_content(dx, dy) is None
        ):
            # Actualizar la celda anterior a None antes de moverse
            self.update_cell(dx, dy, self.cell_content(sx, sy))
            # Reflejar el nuevo posicionamiento del agente en el mapa
            self.update_cell(sx, sy, None)
            return True
        return False
    
    def peek_from(self, x, y, vision_range) -> List[Tuple[int, int, str, int]]:
        """Para una posicion, retorna todo lo que se puede ver desde esa posicion,
        en forma de una tupla (coordenadas del objeto, id del objeto, nitidez)
        """
        top_row = max(0, y - vision_range)
        down_row = min(self.height - 1, y + vision_range)
        leftmost_row = max(0, x - vision_range)
        rightmost_row = min(self.width, x + vision_range)
        visible_squares = [(x, y) for x in range(leftmost_row, rightmost_row) for y in range(top_row, down_row)]
        sights = []
        for cx, cy in visible_squares:
            if cx == x and cy == y:
                continue
            sights.append((cx, cy, self.cell_content(cx, cy), self.get_nitidez(x, y, cx, cy)))
        return sights
    
    def shot(self, agent_id: str, direction: Tuple[int], max_length: int):
        "Returns the id of the object hit by the shot, and the distance covered by the bullet"
        curr_X, curr_Y = self.object_positions[agent_id]
        curr_X += direction[0]
        curr_Y += direction[1]
        for i in range(0, max_length):
            if not self.valid_position(curr_X, curr_Y):
                break
            content = self.cell_content(curr_X, curr_Y)
            if content is not None:
                return content, i + 1
            curr_X += direction[0]
            curr_Y += direction[1]
        return None, max_length
    
    def get_nitidez(self, x, y, cx, cy):
        return 1/math.sqrt((cx - x)**2 + (cy - y)**2)

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