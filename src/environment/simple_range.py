from typing import Any, List, Tuple
from Interfaces.IRange import IRange
from environment.map import Map

class SimpleWalking(IRange):
    "You can walk north, south, east or west as long as is a valid not an occupied square"
    def range(self, map: Map, id: int) -> List[Tuple[Tuple[int, int], int]]:
        current_X, current_Y = map.peek_id(id)
        possible_destinations = [((current_X, current_Y), None)]
        for tpl_x, tpl_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x = current_X + tpl_x
            y = current_Y + tpl_y
            try:
                content = map.peek_from_position((x, y))
                if not content:
                    possible_destinations.append(((x, y), None))
            except:
                continue
        return possible_destinations

class SquareVision(IRange):
    def __init__(self, radius : int):
        self.radius = radius

    def range(self, map: Map, id: int) -> List[Tuple[Tuple[int] | int]]:
        current_X, current_Y = map.peek_id(id)
        vision = []
        upper_row = max(0, current_X - self.radius)
        bottom_row = min(map.height - 1, current_X + self.radius)
        leftmost_column = max(0, current_Y - self.radius)
        rightmost_column = min(map.width - 1, current_Y + self.radius)
        for row in range(upper_row, bottom_row + 1):
            for column in range(leftmost_column, rightmost_column + 1):
                if (row == current_X) and (column == current_Y):
                    continue
                try:
                    vision.append(((row, column), map.peek_from_position((row, column))))
                except:
                    continue
        return vision