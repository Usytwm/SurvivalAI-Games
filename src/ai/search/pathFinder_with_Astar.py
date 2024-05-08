import heapq
from typing import Callable, Tuple


def default_heuristic(A, B):
    return abs(B[0] - A[0]) + abs(B[1] - A[1])

def default_cost_function(A, B, goal):
    return 1

class PathFinder:
    def __init__(
        self,
        validate_movements: Callable[[int, int], bool],
        heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = default_heuristic,
        cost_function: Callable[[Tuple[int, int], Tuple[int, int], Tuple[int, int]], float] = default_cost_function, 
    ):

        self.obstacles = set()  # A set to store obstacle positions
        self.validate_movements = validate_movements
        self.heuristic = heuristic
        self.cost_function = cost_function

    def set_obstacles(self, obstacles):
        self.obstacles = set(obstacles)  # Update obstacle positions

    def a_star(self, start, goal, movements=[(0, 0), (-1, 0), (0, -1), (0, 1), (1, 0)]):
        open_heap = []
        heapq.heappush(open_heap, (0 + self.heuristic(start, goal), 0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while open_heap:
            _, current_cost, current = heapq.heappop(open_heap)

            if current == goal:
                return self.reconstruct_path(came_from, start, goal)

            for move in movements:
                if move == (0, 0):
                    continue  # Ignore the non-moving option in pathfinding
                next = (current[0] + move[0], current[1] + move[1])
                if (
                    self.validate_movements(next[0], next[1])
                    and next not in self.obstacles
                ):
                    new_cost = current_cost + self.cost_function(current, next, goal)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.heuristic(next, goal)
                        heapq.heappush(open_heap, (priority, new_cost, next))
                        came_from[next] = current

        return None  # No path found

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path