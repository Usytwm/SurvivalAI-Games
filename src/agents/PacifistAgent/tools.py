import math
from typing import List, Tuple


def move_away_from_attacker(
    current_pos: Tuple[int, int],
    attacker_pos: Tuple[int, int],
    possible_moves: List[Tuple[int, int]],
) -> Tuple[int, int]:
    x1, y1 = current_pos
    x2, y2 = attacker_pos
    x2 = x1 + x2
    y2 = y1 + y2

    # Inicializar la mejor posición y la mayor distancia encontrada
    best_move = (0, 0)
    max_distance = -float("inf")

    # Evaluar cada movimiento posible
    for move in possible_moves:
        new_x, new_y = x1 + move[0], y1 + move[1]

        # Calcular la distancia desde la nueva posición al atacante
        distance = math.sqrt((x2 - new_x) ** 2 + (y2 - new_y) ** 2)

        # Si la distancia es mayor que la máxima encontrada, actualizar
        if distance > max_distance:
            max_distance = distance
            best_move = move
    return best_move
