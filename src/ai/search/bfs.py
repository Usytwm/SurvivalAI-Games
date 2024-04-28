from typing import Callable, List, Tuple, Set


from typing import Callable, List, Tuple, Set
from collections import deque


class BFS:
    def __init__(self, validate_movements: Callable[[Tuple[int, int]], bool]):
        self.validate_movements = validate_movements
        self.obstacles = set()  # A set to store obstacle positions

    def set_obstacles(self, obstacles: List[Tuple[int, int]]):
        self.obstacles = set(obstacles)  # Update obstacle positions

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def bfs_path(
        self,
        posicion_inicial: Tuple[int, int],
        posicion_atacante: Tuple[int, int],
        posibles_movimientos: List[Tuple[int, int]] = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (0, 0),
        ],
        full_path: bool = False,
    ) -> List[Tuple[int, int]]:
        """
        Implementación de BFS modificada para encontrar el primer paso óptimo o el camino completo más lejano posible del atacante.

        Argumentos:
        posicion_inicial: Tupla que representa la posición inicial del jugador (fila, columna).
        posicion_atacante: Tupla que representa la posición del atacante (fila, columna).
        posibles_movimientos: Lista de tuplas con movimientos posibles desde la posición actual.
        full_path: Booleano que indica si se desea el camino completo o solo el primer paso.

        Retorno:
        Lista de tuplas que representa el camino o el primer paso hasta la posición más lejana del atacante.
        """

        queue = deque(
            [(posicion_inicial, [posicion_inicial])]
        )  # Cola para BFS con caminos
        visited = set()  # Conjunto para mantener registro de las posiciones visitadas
        max_distancia = -1
        mejor_camino = []

        while queue:
            nodo_actual, camino_actual = queue.popleft()
            distancia_actual = self.heuristic(nodo_actual, posicion_atacante)

            # Actualizar el mejor camino si la distancia actual es mayor
            if distancia_actual > max_distancia:
                max_distancia = distancia_actual
                mejor_camino = camino_actual
                if not full_path and len(camino_actual) > 1:
                    return (
                        camino_actual[1] if len(camino_actual) > 1 else camino_actual[0]
                    )

            for movimiento in posibles_movimientos:
                nueva_posicion = (
                    nodo_actual[0] + movimiento[0],
                    nodo_actual[1] + movimiento[1],
                )
                if (
                    nueva_posicion not in visited
                    and nueva_posicion not in self.obstacles
                    and self.validate_movements(nueva_posicion[0], nueva_posicion[1])
                ):
                    visited.add(nueva_posicion)
                    queue.append((nueva_posicion, camino_actual + [nueva_posicion]))

        return (
            mejor_camino
            if full_path
            else (mejor_camino[1] if len(mejor_camino) > 1 else mejor_camino[0])
        )
