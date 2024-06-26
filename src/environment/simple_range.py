from typing import Any, List, Tuple, Dict
from Interfaces.IRange import IRange
from Interfaces.IVision import IVision
from Interfaces.IMovement import IMovement
from Interfaces.IAttack_Range import IAttackRange
from environment.actions import Action_Info, Association_Creation, Action_Type
from environment.map import Map
from environment.sim_object import Sim_Object, Object_Info, Agent_Info, Sim_Object_Type


class SimpleWalking(IMovement):
    "You can walk north, south, east or west as long as is a valid not an occupied square"

    def moves(self, map: Map, id: int) -> List[Tuple[int, int]]:
        current_X, current_Y = map.peek_id(id)
        possible_movements = [(0, 0)]
        for tpl_x, tpl_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x = current_X + tpl_x
            y = current_Y + tpl_y
            try:
                content = map.peek_from_position((x, y))
                if not content:
                    possible_movements.append((tpl_x, tpl_y))
            except:
                continue
        return possible_movements
    
    def pure_moves(self) -> List[Tuple[int]]:
        return [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]


class SquareRange(IRange):
    def __init__(self, radius: int):
        self.radius = radius

    def get_range(self, map: Map, id: int) -> List[Tuple[int, int]]:
        current_X, current_Y = map.peek_id(id)
        return_range = []
        upper_row = max(0, current_X - self.radius)
        bottom_row = min(map.height - 1, current_X + self.radius)
        leftmost_column = max(0, current_Y - self.radius)
        rightmost_column = min(map.width - 1, current_Y + self.radius)
        for row in range(upper_row, bottom_row + 1):
            for column in range(leftmost_column, rightmost_column + 1):
                return_range.append((row, column))
        return return_range


class SquareVision(IVision):
    def __init__(self, radius: int):
        self.range = SquareRange(radius)

    def see_objects(
        self, map: Map, id: int, objects: Dict[int, Sim_Object]
    ) -> List[Object_Info]:
        current_X, current_Y = map.peek_id(id)
        vision = []
        for row, column in self.range.get_range(map, id):
            if (row == current_X) and (column == current_Y):
                continue
            try:
                # O sea si no hay nada en una posicion la pasamos como None
                id = map.peek_from_position((row, column))
                position = (row - current_X, column - current_Y)
                type = objects[id].type
                if type.value == Sim_Object_Type.AGENT.value:
                    vision.append(Agent_Info(position, id, objects[id].reserve))
                vision.append(Object_Info(position, id, objects[id].type))
            except:
                continue
        return vision

    def see_resources(self, map: Map, id: int) -> List[Tuple[Tuple[int, int], int]]:
        current_X, current_Y = map.peek_id(id)
        vision = []
        for row, column in self.range.get_range(map, id):
            vision.append(
                ((row - current_X, column - current_Y), map.resources[(row, column)])
            )
        return vision

    def see_actions(self, map: Map, id: int) -> List[Action_Info]:
        current_X, current_Y = map.peek_id(id)
        vision = []
        for row, column in self.range.get_range(map, id):
            if (row == current_X) and (column == current_Y):
                continue
            try:
                for act in map.last_turn_actions[(row, column)]:
                    match act.type.value:
                        case Action_Type.ASSOCIATION_CREATION.value:
                            vision.append(act)
                        case Action_Type.ASSOCIATION_DESTRUCTION.value:
                            vision.append(act)
                        case Action_Type.ATTACK.value:
                            act.position = (row, column)
                            vision.append(act)
                        case _:
                            vision.append(
                                Action_Info(
                                    (row - current_X, column - current_Y),
                                    act.type,
                                    act.actor_id,
                                    act.destinataries_ids,
                                )
                            )
            except Exception as ex:
                continue
        return vision


class SquareAttackRange(IAttackRange):
    def __init__(self, radius: int):
        self.range = SquareRange(radius)

    def possible_victims(self, map: Map, id: int) -> List[int]:
        current_X, current_Y = map.peek_id(id)
        victims = []
        for row, column in self.range.get_range(map, id):
            if (row == current_X) and (column == current_Y):
                continue
            try:
                victim = map.peek_from_position((row, column))
                if victim:
                    victims.append(victim)
            except Exception as ex:
                continue
        return victims
