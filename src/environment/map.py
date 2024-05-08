import bidict
import os
import sys

current_dir = os.getcwd()
sys.path.insert(0, current_dir + "/src")
sys.path.insert(0, current_dir + "/src/environment")
from typing import Tuple, Dict, List
from actions import Action, Action_Type


class Map:
    def __init__(self, width: int, height: int, resources: Dict[Tuple[int, int], int]):
        self.width = width
        self.height = height
        self.resources = resources  # Says how much sugar there is in a given cell
        self.resources_limit = resources.copy()  # Says how much shugar can be in a cell
        self.max_resources = (
            max(self.resources_limit.values()) if self.resources_limit else 0
        )
        self.last_turn_actions: Dict[Tuple[int, int], List[Action]] = {}
        self.__terrain__ = bidict.bidict()

    def IsValid(self, position: Tuple[int, int]):
        return (
            (position[0] >= 0)
            and (position[0] < self.height)
            and (position[1] >= 0)
            and (position[1] < self.width)
        )

    def resource_percentage(self, position: Tuple[int, int]) -> float:
        """Calculates the percentage of max resources that the current resources in the position represent compared to the maximum in any cell."""
        return (
            (self.resources[position] / self.max_resources)
            if position in self.resources and self.max_resources > 0
            else 0
        )

    def insert(self, position: Tuple[int, int], id: int) -> None:
        "Inserts in a given position an element with the given id"
        if self.IsValid(position):
            if self.__terrain__.get(position, None):
                raise PositionTaken
            try:
                self.__terrain__[position] = id
                return
            except:
                raise IDAlreadyExists
        raise NotValidPosition

    def pop_from_position(self, position: Tuple[int, int]) -> int | None:
        """Remove the element at the given position, and returns its id, or None if there is
        no element at the position"""
        if self.IsValid(position):
            try:
                return self.__terrain__.pop(position)
            except:
                return None
        raise NotValidPosition

    def pop_id(self, id: int) -> Tuple[int, int]:
        "Removes the element with the given id and returns its position"
        try:
            return self.__terrain__.inverse.pop(id)
        except:
            raise IDDoesntExists

    def peek_from_position(self, position: Tuple[int, int]) -> int | None:
        "If there is an element in the given position returns it, otherwise returns None"
        if self.IsValid(position):
            try:
                return self.__terrain__[position]
            except:
                return None
        raise NotValidPosition

    def peek_id(self, id: int) -> Tuple[int, int]:
        "Devuelve la posición de un elemento con el ID dado."
        try:
            return self.__terrain__.inverse[id]
        except:
            raise IDDoesntExists

    def move(self, id: int, new_position: Tuple[int, int]):
        "Moves the element with the given id to a new position"
        self.pop_id(id)
        self.insert(new_position, id)

    def feed(self, id: int):
        """Given the id of an agent, returns the number of resources that there are in its position
        and makes the resources in that position go to 0 (he eats them all)"""
        try:
            position = self.peek_id(id)
            return_value = self.resources[position]
            self.resources[position] = 0
            return return_value
        except:
            raise IDDoesntExists

    def grow(self):
        """Increases the number of resources in each position by one, without exceding the limit
        of any position"""
        for i in range(self.height):
            for j in range(self.width):
                self.resources[(i, j)] = min(
                    self.resources[(i, j)] + 1, self.resources_limit[(i, j)]
                )

    def add_action(self, action: Action):
        if (action.type.value == Action_Type.ATTACK.value):
            print(str(action.actor_id) + " ataca a " + str(action.destinataries_ids[0]) + " with strength " + str(action.strength))
        else:
            if (action.type.value == Action_Type.DIE.value):
                print(str(action.actor_id) + " ha muerto")
        position = self.peek_id(action.actor_id)
        if not position in self.last_turn_actions:
            self.last_turn_actions[position] = []
        self.last_turn_actions[position].append(action)

    def clear_actions(self):
        self.last_turn_actions.clear()


class MapException(Exception):
    pass


class PositionTaken(MapException):
    pass


class IDAlreadyExists(MapException):
    pass


class NotValidPosition(MapException):
    pass


class IDDoesntExists(MapException):
    pass
